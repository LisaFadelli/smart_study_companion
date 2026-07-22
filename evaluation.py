# Version 1.0 Minimal version for evaluation of the Chunking strategy RAG fixed  vs recursive
# Computes the IR metrics (Recall@k, Precision@k, MRR), broken down topic and question type.


import json # save results
from datetime import datetime, timezone
from pathlib import Path # to create folders/files
from collections import defaultdict # group metrics

RUN_LOG_DIR=Path("run_logs")

#IR metrics
def _gold_pages(qa_item):
    gold_pages=set() # empty set to store the gold_sources list
    for g in qa_item["gold_sources"]:
        gold_pages.add((g["source"], g["page"]))
    return gold_pages

def _retrieved_pages(retrieved_docs):
    retrieved_pages=[] # empty list to save the retrieved pages
    for document in retrieved_docs:
        source=document.metadata.get("source")
        page=document.metadata.get("page")
        page_info=(source, page)
        retrieved_pages.append(page_info)
    return retrieved_pages

def score_single_item(qa_item, retriever, match_mode="any"):

    # 1. Retrieve the docs for the question
    question=qa_item["question"]
    docs=retriever.invoke(question)

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

def score_all_items(qa_set, retriever, match_mode="any"):
    """
    Evaluate every question in the QA set.
    For each question:
    1. Retrieve the relevant documents.
    2. Compute the retrieval metrics.
    3. Store the evaluation result.
    Returns a list containing the evaluation results for all questions.
    """

    scored_items = []
    for item in qa_set:
        result = score_single_item(item, retriever, match_mode=match_mode)
        scored_items.append(result)
    return scored_items


# Aggregation, broken down by topic_category and question_type

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


# RAGAS

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

    questions=[]
    answers=[]
    contexts=[]
    ground_truth=[]

    for item in qa_set:
        question=item["question"]
        retrieved_documents=retriever.invoke(question)
        context_texts=[]
        for document in retrieved_documents:
            page_text=document.page_content
            context_texts.append(page_text)
        
        generated_answer=chain.invoke(question)

        questions.append(question)
        answers.append(generated_answer)
        contexts.append(context_texts)
        ground_truth.append(item["gold_answer"])
    
    dataset_dictionary={
        "question":questions,
        "answer":answers,
        "contexts":contexts,
        "ground_truth":ground_truth
    }

    dataset=Dataset.from_dict(dataset_dictionary)

    return dataset

def run_ragas_eval(qa_set, retriever, chain, generation_model, embeddings, temperature):

    from ragas import evaluate
    from ragas.metrics import(faithfulness, context_precision, answer_relevancy,)
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from langchain_google_genai import ChatGoogleGenerativeAI

    def get_judge_llm(model_name, project, temperature=0.2):
        return ChatGoogleGenerativeAI(model=model_name, vertexai=True, project=project, temperature=temperature,)
    
    dataset=build_ragas_dataset(qa_set, retriever, chain)
    judge_llm = get_judge_llm(generation_model, project="smartstudy-thesis", temperature=temperature,)
    ragas_llm = LangchainLLMWrapper(judge_llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

    metrics = [faithfulness, context_precision, answer_relevancy]

    result = evaluate(dataset, metrics=metrics, llm=ragas_llm, embeddings=ragas_embeddings)
    result_dataframe=result.to_pandas()
    return result_dataframe


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

    from store import(get_embeddings, get_vector_store, get_retriever,)
    from rag_chain import build_chain

    # Step 1: create retriever
    from config import resolve_mongo_cfg

    mongo_cfg = resolve_mongo_cfg(cfg)
    embeddings= get_embeddings(cfg["embedding"]["model"])
    vector_store = get_vector_store(mongo_cfg, embeddings)
    retrieval_k=cfg["retrieval"]["k"]
    retriever=get_retriever(vector_store, k=retrieval_k)

    # Step 2: retrieval evaluation
    print(f"[1/3] Scoring retrieval (IR metrics), collection={mongo_cfg['collection_name']}, match_mode={match_mode}")

    scored_items = score_all_items(qa_set, retriever, match_mode=match_mode)
    ir_results = aggregate_results(scored_items)
    print(json.dumps(ir_results["overall"], indent=2))

    # Step 3: Ragas evaluation
    ragas_df=None
    if run_ragas:
        print("[2/3] Running RAGAS evaluation")
        generation_model=cfg["generation"]["model"]
        temperature=cfg["generation"].get("temperature", 0.2)

        chain = build_chain(retriever, generation_model, temperature=temperature)

        ragas_df = run_ragas_eval(qa_set, retriever, chain, generation_model=generation_model, embeddings=embeddings, temperature=temperature)
    else:
        print("Skipping RAGAS")

    # Step 4: Save evaluation results
    print("[3/3] Saving results")

    RUN_LOG_DIR.mkdir(exist_ok=True)

    timestamp = (datetime.now(timezone.utc).isoformat(timespec="seconds").replace(":", "-"))
    strategy = cfg["chunking"]["strategy"]

    log = {}

    log["run_started_utc"] = timestamp
    log["chunking_strategy"] = strategy
    log["match_mode"] = match_mode
    log["k"] = retrieval_k
    log["n_qa_items"] = len(qa_set)
    log["ir_metrics"] = ir_results
    log["per_item"] = scored_items

    log_path = (RUN_LOG_DIR /f"eval_{timestamp}_{strategy}.json")
    log_text = json.dumps(log, indent=2)
    log_path.write_text(log_text)

    print(f"Saved to {log_path}")

    if ragas_df is not None:

        ragas_path = (
            RUN_LOG_DIR /
            f"eval_{timestamp}_{strategy}_ragas.csv"
        )

        ragas_df.to_csv(
            ragas_path,
            index=False
        )

        print(
            f"RAGAS results saved to {ragas_path}"
        )


    return log, ragas_df

if __name__ == "__main__":
    from config import CONFIG
    from qa_set import QA_SET

    run_evaluation(CONFIG, QA_SET, run_ragas=True, match_mode="any")