from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

message="""
You are a Formal Academic Tutor helping a student prepare for an exam. 
Rules you must always follow:
1. Answer only using the context below. If the context does not contain the answer, say so plainly.
2. Always cite the source page(s), in the form (Source:{{source}}, p.{{page}}).
3. After answering, ask a genuine follow-up question.
4. If the student has just proposed their own explanation, definition or claim, \
    you must evaluate it explicitly against the source contexy, confirm what's correct, \
    and gently correct what's innacurate or incomplete before moving on. \
    Do not simply re-answer the original question as if the student's statement wasn't there.
5. If the conversation history shows the student is confused or has asked something similar before, \
    acknowledge that rather than repeating the same explanation verbatim.

Context:
{context}

Question:
{question}

"""

def format_context(docs):
    parts=[]
    for d in docs:
        src=d.metadata.get("source", "unknown")
        page=d.metadata.get("page", "?")
        parts.append(f"[Source: {src}, p.{page}]\n{d.page_content}")
    return "\n\n".join(parts)

def build_chain(retriever, model_name, temperature=0.2): # to wire everything together
    prompt=ChatPromptTemplate.from_template(message)
    llm=ChatGoogleGenerativeAI(model=model_name, project="smartstudy-thesis", vertexai=True, temperature=temperature)

    chain=(RunnableParallel(context=retriever | format_context, question=RunnablePassthrough())
           | prompt
           | llm
           | StrOutputParser()
    )
    return chain

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    from store import get_embeddings, get_vector_store, get_retriever
    from config import CONFIG, resolve_mongo_cfg

    embeddings = get_embeddings(CONFIG["embedding"]["model"])
    vector_store = get_vector_store(resolve_mongo_cfg(CONFIG), embeddings)
    retriever = get_retriever(vector_store, k=CONFIG["retrieval"]["k"])

    chain = build_chain(retriever, CONFIG["generation"]["model"], temperature=CONFIG["generation"].get("temperature", 0.2))
    answer = chain.invoke("What TV game show did IBM's Watson win, and in what year?")
    print(answer)