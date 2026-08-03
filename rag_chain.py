from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # Help to build structured prompts for LLM, including slots for chat history and user input
from langchain_core.output_parsers import StrOutputParser # Tell the chain to return plain text from the LLM
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List, Tuple
 

### 1) Condensation step: turn a follow up question so into a query
# This prompt is used to rewrite a follow-up question so it can be understood without needing the chat history.
#
# The LLM is instructed NOT to answer, only to rewrite.
_CONDENSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Given a chat history and a follow-up question, rewrite the follow-up into a standalone question that can be understood without the chat "
     "history. Do not answer the question, only rewrite it. If the question is already standalone, return it unchanged."),
    # This placeholder will be filled with the list of previous messages (the chat history).
    MessagesPlaceholder("chat_history"),
    # This is the current user question.
    ("human", "{question}"),
])

def build_condenser(model_name: str, temperature: float = 0.0):
    """
    Builds and returns a small, cheap LLM chain whose only job is to rewrite (condense) follow-up questions into standalone questions.

    Why separate?
    - We use a low-temperature, focused prompt just for rewriting.
    - This keeps the main generation model free to focus on answering.

    Parameters
    - model_name: which Vertex AI model to use for condensation.
    - temperature: controls randomness; 0.0 = very deterministic.
    """
    # Create the LLM instance for condensation.
    llm=ChatGoogleGenerativeAI(model=model_name, project="smartstudy-thesis", vertexai=True, temperature=temperature)

    # Build a chain: prompt -> LLM -> parse output as string.
    return _CONDENSE_PROMPT | llm | StrOutputParser()

def tuples_to_messages(history: List[Tuple[str, str]]) -> List[BaseMessage]:
    """
    Convert [("human", "..."), ("ai", "...")] tuples (as received over
    the /chat HTTP API) into LangChain message objects for MessagesPlaceholder.

    Unrecognized roles are treated as human input rather than silently
    dropped, so a malformed frontend payload degrades gracefully instead
    of losing a turn.
    """
    messages: List[BaseMessage] = []
    for role, content in history:
        if role == "ai":
            messages.append(AIMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))
    return messages


### 2) Generation step: the main tutor that answers using retrieved context
# This prompt defines the tutor persona and how it should behave.
# Key rules:
# - Answer ONLY using the provided context (no made-up info).
# - Always cite the source file and page number.
# - If context is insufficient, say so explicitly.
# - After answering, ask a short follow-up to check understanding.

# Previous Version
# message="""
# You are a Formal Academic Tutor helping a student prepare for an exam. 
# Rules you must always follow:
# 1. Answer only using the context below. If the context does not contain the answer, say so plainly.
# 2. Always cite the source page(s), in the form (Source:{{source}}, p.{{page}}).
# 3. After answering, ask a genuine follow-up question.
# 4. If the student has just proposed their own explanation, definition or claim, \
#     you must evaluate it explicitly against the source contexy, confirm what's correct, \
#     and gently correct what's inacurate or incomplete before moving on. \
#     Do not simply re-answer the original question as if the student's statement wasn't there.
# 5. If the conversation history shows the student is confused or has asked something similar before, \
#     acknowledge that rather than repeating the same explanation verbatim.

# Context:
# {context}

# Question:
# {question}

# """

_TUTOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a Formal Academic Tutor specialising in the EPSO AD5 competition (Graduates / Administrators). Your role is to help "
     "candidates prepare for the AD5 selection process. You must always follow these rules:\n"
     "1. Answer using ONLY the provided context. If the context does not contain the answer, say so explicitly rather than using general knowledge.\n"
     "2. Always cite the source file and page number in the same form as in the context, e.g. [Source: filename.pdf, p.3].\n"
     "3. After answering, ask a brief follow-up question to check the candidate's understanding.\n"
     "4. Keep all explanations strictly within the scope of the EPSO AD5 competition (e.g., reasoning tests, EU knowledge, digital skills, EUFTE essay, eligibility, timeline, test structure, scoring). If a question is outside this scope, say that it is outside the AD5 scope instead of answering generally."),
    # Include the chat history so the tutor can refer to earlier turns.
    MessagesPlaceholder("chat_history"),
    # The actual user question plus the retrieved context.
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])


def format_context(docs):
    parts=[]
    for d in docs:
        src=d.metadata.get("source", "unknown")
        page=d.metadata.get("page", "?")
        parts.append(f"[Source: {src}, p.{page}]\n{d.page_content}")
    return "\n\n".join(parts)


import logging
logger = logging.getLogger("rag_chain")

def build_chain(retriever, model_name, temperature=0.2): # to wire everything together
    prompt=_TUTOR_PROMPT
    llm=ChatGoogleGenerativeAI(model=model_name, project="smartstudy-thesis", vertexai=True, temperature=temperature)
    condenser=build_condenser(model_name)

    # Decide whether to rewrite the question or just use it as-is.
    # Condition:
    #   - If chat_history is empty (first turn), we don't need to rewrite. We just take x["question"].
    #   - If chat_history is not empty, we run the condenser to get a standalone version of the question.
    condense_or_passthrough = RunnableBranch(
        # Condition + action if True:
        (lambda x: len(x.get("chat_history", [])) == 0, lambda x: x["question"]),
        # Action if False: run the condenser chain.
        condenser,
    )

    def safe_standalone_question(x):
        """
        Run condensation, but never let an empty/blank result reach the
        retriever — the embedding API rejects empty strings outright
        (400 INVALID_ARGUMENT: Empty instances), which is a hard crash,
        not a graceful degradation.
        """
        result = condense_or_passthrough.invoke(x)
        if not result or not result.strip():
            logger.warning("Condenser returned empty result, falling back to raw question")
            return x["question"]
        return result

    chain = (RunnablePassthrough.assign(chat_history=lambda x: tuples_to_messages(x.get("chat_history",[]))) # 1. Convert chat history from tuples -> BaseMessage object
             | RunnablePassthrough.assign(standalone_question=safe_standalone_question) # 2. Condense question + history into a standalone question
             | RunnablePassthrough.assign(context=lambda x: format_context(retriever.invoke(x["standalone_question"]))) # 3. Retrieve context using the standalone question
             | prompt
             | llm
             | StrOutputParser())

    return chain

# Previous Version 
    # chain=(RunnableParallel(context=retriever | format_context, question=RunnablePassthrough())
    #        | prompt
    #        | llm
    #        | StrOutputParser()
    # )
    # return chain

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
#     from store import get_embeddings, get_vector_store, get_retriever
#     from config import CONFIG, resolve_mongo_cfg

#     embeddings = get_embeddings(CONFIG["embedding"]["model"])
#     vector_store = get_vector_store(resolve_mongo_cfg(CONFIG), embeddings)
#     retriever = get_retriever(vector_store, k=CONFIG["retrieval"]["k"])

#     chain = build_chain(retriever, CONFIG["generation"]["model"], temperature=CONFIG["generation"].get("temperature", 0.2))
#     answer = chain.invoke({"question": "What tests are included in the EPSO AD5 competition?,"chat_history": []})
#     print(answer)