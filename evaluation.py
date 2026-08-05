"""
evaluation.py
 
Evaluation pipeline for the local RAG system.
Answers thesis sub-questions 1 and 2 (chunking, retrieval).
 
Two things get evaluated:
- IR metrics: Recall@k, Precision@k, MRR, hit rate.
- RAGAS metrics: Faithfulness, Context Precision, Answer Relevancy.
 
One side effect: usage/cost/latency events get logged.
- Logged to MongoDB, collection "usage_metrics".
- "retrieve" events come from the IR step. No cost, latency only.
- "condense"/"generate" events come from the RAGAS step only.
- If run_ragas=False, no generation events are logged.

Results are saved locally, not to MongoDB.
- run_logs/eval_<timestamp>_<tag>.json -> IR metrics
- run_logs/eval_<timestamp>_<tag>_ragas.csv -> RAGAS scores

"""

import json # save results
import time
from datetime import datetime, timezone
from pathlib import Path # to create folders/files
from collections import defaultdict # group metrics
from tqdm import tqdm

from metrics import make_metrics_ctx, log_usage

RUN_LOG_DIR=Path("run_logs")


# ============================================================
# IR METRICS -helpers
# ============================================================

def _gold_pages(qa_item):
    # Build the set of correct (source, page) pairs for one question.
    gold_pages=set() # empty set to store the gold_sources list
    for g in qa_item["gold_sources"]:
        gold_pages.add((g["source"], g["page"]))
    return gold_pages

def _retrieved_pages(retrieved_docs):
    # Turn retrieved LangChain docs into a list of (source, page) pairs.
    retrieved_pages=[] # empty list to save the retrieved pages
    for document in retrieved_docs:
        source=document.metadata.get("source")
        page=document.metadata.get("page")
        page_info=(source, page)
        retrieved_pages.append(page_info)
    return retrieved_pages


# ============================================================
# IR METRICS -- per question
# ============================================================

def score_single_item(qa_item, retriever, match_mode="any", metrics_ctx=None):
    """
    Score one question against the retriever. Returns a dict with hit / recall / precision / MRR.
    """

    # 1. Retrieve the docs for the question, times
    question=qa_item["question"]
    start=time.monotonic()
    docs=retriever.invoke(question)
    elapsed=time.monotonic()-start

    if metrics_ctx is not None:
        # "mongodb_atlas_retrieval" has no pricing entry. cost_usd is always 0.0 for this component. Latency only.
        log_usage(model="mongodb_atlas_retrieval", component="retrieve", latency_seconds=elapsed, metrics_ctx=metrics_ctx, extra={"qa_id": qa_item["qa_id"]},)

    # 2. Extract source and page info
    retrieved_pages=_retrieved_pages(docs)
    retrieved_pages_set=set(retrieved_pages) # Algo4BG class: set allows faster checking
    gold_page=_gold_pages(qa_item)

    # 3. Find pages that were correctly retrieved
    matching_page=set()
    for gold in gold_page:
        if gold in retrieved_pages_set:
            matching_page.add(gold)

    # 4. Determine if this question is a "hit"
    if match_mode=="any": # the question is considered solved if at least one correct page was retrieved
        hit=len(matching_page)>0
    elif match_mode=="all": # the question is considered solved only if every required page was retrieved
        hit = True
        for gold in gold_page:
            if gold not in retrieved_pages_set:
                hit=False
                break
    else:
        raise ValueError(f"Unknown match_mode: {match_mode}")


    # 5. Calculating Recall@K -> "how many of the required answer pages did the retriever find?"
    if len(gold_page)>0:
        recall_at_k=len(matching_page)/len(gold_page)
    else:
        recall_at_k=0.0
    
    # 6. Calculating Precision@K -> "among retrieved pages, how many were useful?"
    if len(retrieved_pages)>0:
        precision_at_k=len(matching_page)/len(retrieved_pages)
    else:
        precision_at_k=0.0
    
    # 7. Calculate Reciprocal Rank (MRR) -> "how early the first doc appears?"
    mrr=0.0 # default
    for rank in range(len(retrieved_pages)):
        current_rank=rank+1
        current_page=retrieved_pages[rank]
        if current_page in gold_page:
            mrr=1/current_rank
            break
    
    # 8. Prepare evaluation
    result= {
        "qa_id": qa_item["qa_id"],
        "topic_category": qa_item.get("topic_category"),
        "question_type": qa_item["question_type"],
        "hit": hit,
        "recall_at_k": recall_at_k,
        "precision_at_k": precision_at_k,
        "reciprocal_rank": mrr,
        "retrieved_pages": retrieved_pages,
        "gold_pages": sorted(gold_page),
    }
    return result


def score_all_items(qa_set, retriever, match_mode="any", metrics_ctx=None):
    """
    Evaluate every question in the QA set.
    For each question:
    1. Retrieve the relevant documents.
    2. Compute the retrieval metrics.
    3. Store the evaluation result.
    Returns a list containing the evaluation results for all questions.
    """
    scored_items = []
    for item in tqdm(qa_set, "Running IR metrics"):
        result = score_single_item(item, retriever, match_mode=match_mode, metrics_ctx=metrics_ctx)
        scored_items.append(result)
    return scored_items


# ============================================================
# IR METRICS -- aggregation
# ============================================================

def _aggregate(records):
    """This function takes the evaluation results for multiple questions and computes the average metrics."""
    if not records:
        return {"n": 0, "recall_at_k": None, "precision_at_k": None, "mrr": None, "hit_rate": None}
    
    n = len(records)
    return {
        "n": n,
        "recall_at_k": sum(r["recall_at_k"] for r in records)/n,
        "precision_at_k": sum(r["precision_at_k"] for r in records)/n,
        "mrr": sum(r["reciprocal_rank"] for r in records)/n,
        "hit_rate": sum(1 for r in records if r["hit"])/n,
    }


def aggregate_results(scored_records):
    # Overall average, plus broken down by topic and question type.
    overall = _aggregate(scored_records)

    by_topic = defaultdict(list)
    by_type = defaultdict(list)
    for r in scored_records:
        by_topic[r["topic_category"]].append(r)
        by_type[r["question_type"]].append(r)

    return {
        "overall": overall,
        "by_topic_category": {k: _aggregate(v) for k, v in by_topic.items()},
        "by_question_type": {k: _aggregate(v) for k, v in by_type.items()},
    }


# ============================================================
# RAGAS -- dataset building
# ============================================================

def build_ragas_dataset(qa_set, retriever, chain):
    """
    Build the dataset in the format expected by RAGAS.
    For each question:
    1. Retrieve the relevant documents
    2. Extract the retrieved context
    3. Generate answer using the RAG chain
    4. Store everything in lists
    """
    from datasets import Dataset # from HuggingFace library provides an easy way to create, load, manipulate datasets for ML workflows

    qa_ids=[]
    questions=[]
    answers=[]
    contexts=[]
    ground_truth=[]

    for item in tqdm(qa_set, desc="Building RAGAS dataset", unit="q"):
        # 1: retrieve context for this question
        question = item["question"]
        retrieved_documents = retriever.invoke(question)
        context_texts = [doc.page_content for doc in retrieved_documents]
 
        # 2: generate the answer with the full chain
        generated_answer = chain.invoke({"question": question, "chat_history": []})
 
        # 3: collect everything
        qa_ids.append(item["qa_id"])
        questions.append(question)
        answers.append(generated_answer)
        contexts.append(context_texts)
        ground_truth.append(item["gold_answer"])
 
    dataset_dictionary = {
        "qa_id": qa_ids,
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truth,
    }
    return Dataset.from_dict(dataset_dictionary)


# ============================================================
# RAGAS -- scoring
# ============================================================

def run_ragas_eval(qa_set, retriever, chain, generation_model, embeddings, temperature):
    """
    Score the RAGAS dataset with Faithfulness, Context Precision, Answer Relevancy.
    """
    from ragas import evaluate
    from ragas.metrics import faithfulness, context_precision, answer_relevancy
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from langchain_google_genai import ChatGoogleGenerativeAI

    def get_judge_llm(model_name, project, temperature=0.2):
        return ChatGoogleGenerativeAI(model=model_name, vertexai=True, project=project, temperature=temperature,)

    # 1: build the dataset (this generates answers)
    dataset=build_ragas_dataset(qa_set, retriever, chain)
    qa_ids=[item["qa_id"] for item in qa_set]

    # 2: set up the RAGAS judge 
    judge_llm = get_judge_llm(generation_model, project="smartstudy-thesis", temperature=temperature,)
    ragas_llm = LangchainLLMWrapper(judge_llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    metrics = [faithfulness, context_precision, answer_relevancy]

    # 3: run RAGAS scoring
    result = evaluate(dataset, metrics=metrics, llm=ragas_llm, embeddings=ragas_embeddings)
    result_dataframe=result.to_pandas()

    # 4: check row alignment before reattaching qa_id
    if len(result_dataframe) != len(qa_ids):
        raise RuntimeError(
            f"RAGAS returned {len(result_dataframe)} rows but {len(qa_ids)} questions "
            "were submitted to evaluate(). Row alignment cannot be assumed. "
            "Some items likely failed silently inside ragas. "
            "Inspect the run before reattaching qa_id."
        )
    result_dataframe.insert(0, "qa_id", qa_ids)
    return result_dataframe


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def run_evaluation(cfg, qa_set, run_ragas=True, match_mode="any"):
    """
    Run the complete evaluation pipeline:
    1. Loading the vector database
    2. Computing retrieval metrics
    3. Running RAGAS
    4. Saving the results
    """

    from dotenv import load_dotenv
    load_dotenv()

    from store import get_embeddings, get_vector_store, get_retriever
    from rag_chain import build_chain
    from metrics import make_metrics_ctx
    from config import resolve_mongo_cfg

    # 1: create retriever
    mongo_cfg = resolve_mongo_cfg(cfg)
    embeddings= get_embeddings(cfg["embedding"]["model"])
    vector_store = get_vector_store(mongo_cfg, embeddings)
    retrieval_k=cfg["retrieval"]["k"]
    retriever = get_retriever(vector_store, k=retrieval_k,strategy=cfg["retrieval"]["strategy"],collection=vector_store.collection, mongo_cfg=mongo_cfg,)

    # 2: one shared metrics_ctx for the whole run
    metrics_ctx = make_metrics_ctx(chunking_strategy=cfg["chunking"]["strategy"],retrieval_strategy=cfg["retrieval"]["strategy"],run_id=f"eval_{cfg['chunking']['strategy']}_{cfg['retrieval']['strategy']}",)

    # 3: IR metrics
    print(f"[1/3] Scoring retrieval (IR metrics), collection={mongo_cfg['collection_name']}, match_mode={match_mode}")  
    scored_items = score_all_items(qa_set, retriever, match_mode=match_mode, metrics_ctx=metrics_ctx)
    ir_results = aggregate_results(scored_items)
    print(json.dumps(ir_results["overall"], indent=2))

    # 4: Ragas evaluation
    ragas_df=None
    if run_ragas:
        print("[2/3] Running RAGAS evaluation")
        generation_model=cfg["generation"]["model"]
        temperature=cfg["generation"].get("temperature", 0.2)

        chain = build_chain(retriever, generation_model, temperature=temperature,metrics_ctx=metrics_ctx)
        ragas_df = run_ragas_eval(qa_set, retriever, chain, generation_model=generation_model, embeddings=embeddings, temperature=temperature)
    else:
        print("Skipping RAGAS")

    # 5: Save evaluation results
    print("[3/3] Saving results")
    RUN_LOG_DIR.mkdir(exist_ok=True)
    timestamp = (datetime.now(timezone.utc).isoformat(timespec="seconds").replace(":", "-"))
    tag = f"{cfg['chunking']['strategy']}_{cfg['retrieval']['strategy']}"

    log = {
        "run_started_utc": timestamp,
        "chunking_strategy": cfg["chunking"]["strategy"],
        "match_mode": match_mode,
        "k": retrieval_k,
        "n_qa_items": len(qa_set),
        "ir_metrics": ir_results,
        "per_item": scored_items,
    }

    log_path = (RUN_LOG_DIR /f"eval_{timestamp}_{tag}.json")
    log_text = json.dumps(log, indent=2)
    log_path.write_text(log_text)
    print(f"Saved to {log_path}")

    if ragas_df is not None:
        ragas_path = (RUN_LOG_DIR / f"eval_{timestamp}_{tag}_ragas.csv")
        ragas_df.to_csv(ragas_path, index=False)
        print(f"RAGAS results saved to {ragas_path}")
    return log, ragas_df

if __name__ == "__main__":
    from config import CONFIG
    from qa_set import QA_SET
    run_evaluation(CONFIG, QA_SET, run_ragas=True, match_mode="any")