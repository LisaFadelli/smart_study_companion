import logging
from typing import List, Tuple
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from metrics import log_usage

logger = logging.getLogger("rag_chain")

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
    Builds and returns a LLM chain whose only job is to rewrite (condense) follow-up questions into standalone questions.

    Why separate?
    - We use a low-temperature, focused prompt just for rewriting.
    - This keeps the main generation model free to focus on answering.

    Parameters
    - model_name: which Vertex AI model to use for condensation.
    - temperature: controls randomness; 0.0 = very deterministic.
    """
    # Create the LLM instance for condensation.
    llm=ChatGoogleGenerativeAI(model=model_name, project="smartstudy-thesis", vertexai=True, temperature=temperature)

    def _timed_invoke(prompt_value) -> AIMessage:
        """Times the condenser's own LLM call and logs its token usage."""
        start = time.monotonic()
        message = llm.invoke(prompt_value)
        elapsed = time.monotonic() - start
        if metrics_ctx is not None:
            usage = getattr(message, "usage_metadata", None) or {}
            log_usage(
                model=model_name,
                component="condense",
                latency_seconds=elapsed,
                metrics_ctx=metrics_ctx,
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
            )
        return message
    
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
    if not history:
        return messages

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



def build_chain(retriever, model_name, temperature=0.2, metrics_ctx=None): # to wire everything together
    prompt=_TUTOR_PROMPT
    llm=ChatGoogleGenerativeAI(model=model_name, project="smartstudy-thesis", vertexai=True, temperature=temperature)
    condenser=build_condenser(model_name, metrics_ctx=metrics_ctx)

    def safe_standalone_question(x):
        """
       Safely generates a standalone question. 
        Catches empty strings, whitespace, and LLM exception blocks to guarantee 
        a valid non-empty string reaches the embedding retriever.
        """
        raw_question = str(x.get("question", "")).strip()
        messages_history = x.get("chat_history", [])

        # Turn 1: If chat_history is empty, return raw question immediately
        if not messages_history:
            return raw_question

        # Turn 2+: Run condenser inside a try/except guard
        try:
            condensed = condenser.invoke(x)
            if isinstance(condensed, str) and condensed.strip():
                return condensed.strip()
            
            logger.warning("Condenser returned empty output or whitespace. Falling back to raw question.")
        except Exception as e:
            logger.error(f"Condenser invocation failed: {e}. Falling back to raw question.")

        # Emergency Fallback: Ensure raw_question itself isn't empty
        if not raw_question:
            raise ValueError("Both condensed standalone question and original user question are empty.")

        return raw_question

    def retrieve_and_format(x: dict) -> str:
        """Retrieves documents using the guaranteed valid standalone question."""
        standalone_q = x["standalone_question"]
        docs = retriever.invoke(standalone_q)
        return format_context(docs)

    def timed_llm_call(prompt_value):
        """Wraps the main tutor LLM call so latency and token usage are
        captured together -- doing this as one step (rather than timing
        outside the chain) avoids folding prompt-formatting time into
        "generation latency"."""
        start = time.monotonic()
        message = llm.invoke(prompt_value)
        elapsed = time.monotonic() - start
        if metrics_ctx is not None:
            usage = getattr(message, "usage_metadata", None) or {}
            log_usage(
                model=model_name,
                component="generate",
                latency_seconds=elapsed,
                metrics_ctx=metrics_ctx,
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
            )
        return message

    chain = (
        # 1. Convert tuple history to BaseMessage objects
        RunnablePassthrough.assign(
            chat_history=lambda x: tuples_to_messages(x.get("chat_history", []))
        )
        # 2. Derive standalone question with robust fail-safes
        | RunnablePassthrough.assign(standalone_question=safe_standalone_question)
        # 3. Retrieve and format vector store documents
        | RunnablePassthrough.assign(context=retrieve_and_format)
        # 4. Generate answer with Tutor LLM
        | prompt
        | llm
        | StrOutputParser()
    )

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