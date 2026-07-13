import os
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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


def upsert_chunks(vector_store, chunks):
    texts = [c["text"] for c in chunks]
    metadatas = [{"page": c["page"], "source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]
    ids=[c["text"] for c in chunks]
    return vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
# Re-running ingestion on the same PDF replaces existing chunks in place instead of inserting duplicates 

def get_retriever(vector_store, k):
    return vector_store.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    mongo_cfg = {
        "db_name": "smartstudy",
        "collection_name": "chunks",
        "vector_index_name": "vector_index",
        "embedding_field": "embedding",
        "text_field": "text",
    }

    emb = get_embeddings(CONFIG["embedding"]["model"])
    print("Embeddings client OK")

    vector_store = get_vector_store(mongo_cfg, emb)
    print("Vector store connection OK")

    test_chunks = [
        {"text": "This is a test chunk about the Louvre Museum.", "page": 1, "source": "test.pdf", "chunk_id": "test_p1_c0"}
    ]
    ids = upsert_chunks(vector_store, test_chunks)
    print(f"Upserted {len(ids)} test document(s), id(s): {ids}")