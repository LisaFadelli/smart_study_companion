from dotenv import load_dotenv
load_dotenv()

from phase0.store import get_embeddings, get_vector_store, get_retriever
from phase0.rag_chain import build_chain
from config import CONFIG, resolve_mongo_cfg

def main():
    mongo_cfg = resolve_mongo_cfg(CONFIG)
    print(f"Querying collection:  {mongo_cfg["collection_name"]}")
    embeddings = get_embeddings(CONFIG["embedding"]["model"])
    vector_store = get_vector_store(mongo_cfg, embeddings)
    retriever = get_retriever(vector_store, k=CONFIG["retrieval"]["k"])
    chain = build_chain(retriever, CONFIG["generation"]["model"], temperature=CONFIG["generation"].get("temperature", 0.2))

    print("SmartStudy baseline tutor. Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        print(f"\nTutor: {chain.invoke(question)}\n")

if __name__ == "__main__":
    main()