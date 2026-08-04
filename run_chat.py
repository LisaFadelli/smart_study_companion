from dotenv import load_dotenv
load_dotenv()

from store import get_embeddings, get_vector_store, get_retriever
from rag_chain import build_chain
from config import CONFIG, resolve_mongo_cfg

def main():
    mongo_cfg = resolve_mongo_cfg(CONFIG)
    print(f"Querying collection:  {mongo_cfg["collection_name"]}")
    embeddings = get_embeddings(CONFIG["embedding"]["model"])
    vector_store = get_vector_store(mongo_cfg, embeddings)
    retriever = get_retriever(vector_store=vector_store, k=CONFIG["retrieval"]["k"], strategy=CONFIG["retrieval"]["strategy"], collection=vector_store.collection, mongo_cfg=mongo_cfg)

    print(f"Retrieval strategy: {CONFIG["retrieval"]["strategy"]}")
    chain = build_chain(retriever, CONFIG["generation"]["model"], temperature=CONFIG["generation"].get("temperature", 0.2))

    print("SmartStudy baseline tutor. Type 'exit' to quit.\n")
    chat_history=[] # fix: added to respect the chat_history requirement and mirror it locally
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        answer = chain.invoke({"question": question, "chat_history": chat_history})
        print(f"\nTutor: {answer}\n")

        # NEW: append this turn so the next one has real history to condense against
        chat_history.append(("human", question))
        chat_history.append(("ai", answer))

if __name__ == "__main__":
    main()