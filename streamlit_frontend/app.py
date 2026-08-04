"""
AI Study Companion - beginner.friendly Streamlit frontend

This app:
- shows a simple chat interface
- sends the user's question + history to your already-deployed Cloud Run chat service
- displays the answer in the chat

"""

import time
import requests
import streamlit as st
from typing import List, Tuple

# 1. Page configuration
st.set_page_config(
    page_title="SmartStudy Tutor",
    page_icon="📚"
)

AVATAR_USER = "🧑‍💻"
AVATAR_ASSISTANT = "🇪🇺"

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #003399;
        color: white;
        font-weight: 600;
        border: none;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: #F2F5FC;
        border: 1px solid #b5c8e8;
        border-radius: 10px;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #FFFBEA;
        border: 1px solid #FFCC00;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:2rem;">📚</span>
        <h1 style="margin:0; color:#003399;">SmartStudy Tutor</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("EPSO EU career exam prep — ask a question about your uploaded lecture material.")

# 2. Chat service URL
# For now, this is hardcoded.
# Later you can move it to st.secrets["chat_endpoint"] or an environment variable.
CHAT_ENDPOINT = "https://smartstudy-chat-696105472724.europe-west1.run.app/chat"

# 3. Sidebar (optional debug / latency info)
with st.sidebar:
    st.header("Debug")

    # Checkbox to show/hide debug info
    debug_mode = st.checkbox("Show retrieval/timing details", value=False)

    # Initialize a list to store recent response times
    if "latencies" not in st.session_state:
        st.session_state.latencies = []

    # Show last 10 response times if we have any
    if st.session_state.latencies:
        st.write("Recent response times (seconds):")
        st.write(st.session_state.latencies[-10:])

    # End chat button
    if st.button("End chat"):
        st.session_state.messages=[]
        st.rerun()

# 4. Chat history management
# Initialize chat history in session state if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for msg in st.session_state.messages:
    avatar = AVATAR_USER if msg["role"] == "user" else AVATAR_ASSISTANT
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Helper: convert Streamlit messages → [(role, content)] tuples for the backend
def build_history_tuples(messages: List[dict]) -> List[Tuple[str, str]]:
    """
    Convert Streamlit-style messages:
      [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    into backend-style history:
      [("human", "..."), ("ai", "...")]
    """
    history = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            history.append(("human", content))
        elif role == "assistant":
            history.append(("ai", content))
        # ignore any other roles
    return history


# Helper: trim history to max_turns
def trim_history_by_turns(
    history: List[Tuple[str, str]],
    max_turns: int = 7,
) -> List[Tuple[str, str]]:
    if not history:
        return []
    return history[-max_turns:]

# 5. Handle new user input
if query := st.chat_input("Ask a question..."):

    # 5.1 Build history tuples
    history_tuples=build_history_tuples(st.session_state.messages)
    history_trimmed=trim_history_by_turns(history_tuples, max_turns=7)

    # 5.2 Add user message to history and show it
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(query)

    # 5.3 Show a "Thinking..." placeholder for the assistant
    with st.chat_message("assistant", avatar=AVATAR_ASSISTANT):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")

        success=False
        answer=None

        try:
            start_time = time.time()

            response = requests.post(
                CHAT_ENDPOINT,
                json={"query": query, "history":history_trimmed},
                timeout=60  # wait up to 60 seconds
            )

            elapsed_time = time.time() - start_time
            st.session_state.latencies.append(round(elapsed_time, 2))

            # 5.4 Handle successful response
            if response.status_code == 200:
                # Try to get the "answer" field from JSON
                data = response.json()
                answer = data.get("answer", "(no answer field in response)")

                placeholder.markdown(answer)
                success=True

                # Optional debug info
                if debug_mode:
                    st.caption(f"Response time: {elapsed_time:.2f}s | HTTP {response.status_code}")

            # 5.5 Handle non-200 responses
            else:
                # Try to get an error detail; if not available, use raw text
                try:
                    error_detail = response.json().get("detail", response.text)
                except Exception:
                    error_detail = response.text

                placeholder.error(f"Service error ({response.status_code}): {error_detail}")

        # 5.6 Handle network/connection errors
        except requests.exceptions.RequestException as e:
            placeholder.error(f"Could not reach the chat service: {e}")

    # 5.7 Add assistant message to history
    if success:
        st.session_state.messages.append({"role": "assistant", "content": answer})