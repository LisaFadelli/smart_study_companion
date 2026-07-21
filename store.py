import os
import time
from datetime import datetime, timezone

from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted

from config import CONFIG

def get_embeddings(model_name):
    return GoogleGenerativeAIEmbeddings(model=model_name, project="smartstudy-thesis", vertexai=True)
# Turn sentences into lists of numbers

def get_vector_store(mongo_cfg, embeddings):
    client=MongoClient(os.environ["MONGODB_URI"])
    collection=client[mongo_cfg["db_name"]][mongo_cfg["collection_name"]]
    return MongoDBAtlasVectorSearch(collection=collection,
        embedding=embeddings,
        index_name=mongo_cfg["vector_index_name"],
        embedding_key=mongo_cfg["embedding_field"],
        text_key=mongo_cfg["text_field"],)
# 1. Opens a connection to my MongoDB Atlas database, using the password/link saved in .env 
# 2. Points at the specific "drawer" inside it where your chunks will live
# 3. Wraps that drawer together with the "number machine" from step 1, so this one object can now do both: turn text into numbers AND save/search them in Atlas

def clear_source(vectore_store, source):
    result=vectore_store.collection.delete_many({"source":source})
    return result.deleted_count
# Delete all existing chunks for a given source PDF before re-ingesting
# Calling this before ingestion guarantees a clean slate per source/config

# To overcome the 429 RESOURCE_EXHAUSTED error
# Re-running ingestion on the same PDF replaces existing chunks in place instead of
# inserting duplicates (idempotent via chunk_id). Batched + retried to stay under
# Vertex AI's embedding quota; batch_log feeds RQ4 latency/throughput analysis.

@retry(
    retry=retry_if_exception_type(ResourceExhausted),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(6),
)

def _add_batch(vector_store, texts, metadatas, ids):
    return vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

def upsert_chunks(vector_store, chunks, batch_size=20, sleep_seconds=2.0):
    all_ids = []
    batch_log = []

    n_batches = (len(chunks) + batch_size - 1) // batch_size

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_num = i // batch_size + 1

        texts = [c["text"] for c in batch]
        metadatas = [{"page": c["page"], "source": c["source"], "chunk_id": c["chunk_id"]} for c in batch]
        ids = [c["chunk_id"] for c in batch]

        start = time.monotonic()
        batch_ids = vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        elapsed = time.monotonic() - start

        all_ids.extend(batch_ids)
        batch_log.append({
            "batch_num": batch_num,
            "batch_size": len(batch),
            "elapsed_seconds": round(elapsed, 3),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        print(f"  Batch {batch_num}/{n_batches}: {len(batch)} chunks in {elapsed:.2f}s")

        if batch_num < n_batches:
            time.sleep(sleep_seconds)

    return all_ids, batch_log

# def upsert_chunks(vector_store, chunks):
#     texts = [c["text"] for c in chunks]
#     metadatas = [{"page": c["page"], "source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]
#     ids = [c["chunk_id"] for c in chunks]
#     return vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
# Re-running ingestion on the same PDF replaces existing chunks in place instead of inserting duplicates 

def get_retriever(vector_store, k):
    return vector_store.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    from config import resolve_mongo_cfg

    mongo_cfg = resolve_mongo_cfg(CONFIG)
    print(f"Using collection: {mongo_cfg['collection_name']}")

    emb = get_embeddings(CONFIG["embedding"]["model"])
    print("Embeddings client OK")

    vector_store = get_vector_store(mongo_cfg, emb)
    print("Vector store connection OK")

    test_chunks = [
        {"text": "This is a test chunk about the Louvre Museum.", "page": 1, "source": "test.pdf", "chunk_id": "test_p1_c0"}
    ]
    ids, batch_log = upsert_chunks(vector_store, test_chunks)
    print(f"Upserted {len(ids)} test document(s), id(s): {ids}")
    print(f"Batch log: {batch_log}")