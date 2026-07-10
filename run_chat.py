from dotenv import load_dotenv
load_dotenv()

from store import get_embeddings, get_vector_store, get_retriever
from rag_chain import build_chain
from config import CONFIG

def main():
    embeddings = get_embeddings(CONFIG["embedding"]["model"])
    vector_store = get_vector_store(CONFIG["mongodb"], embeddings)
    retriever = get_retriever(vector_store, k=CONFIG["retrieval"]["k"])
    chain = build_chain(retriever, CONFIG["generation"]["model"])

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