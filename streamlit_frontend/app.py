"""
AI Study Companion - beginner.friendly Streamlit frontend

This app:
- shows a simple chat interface
- sends the user's question to your already-deployed Cloud Run chat service
- displays the answer in the chat

"""

import time
import requests
import streamlit as st

# 1. Page configuration
st.set_page_config(
    page_title="SmartStudy Tutor",
    page_icon="📚"
)
st.title("📚 SmartStudy Tutor")
st.caption("Ask a question about your uploaded lecture material.")

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

# 4. Chat history management
# Initialize chat history in session state if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Handle new user input
if query := st.chat_input("Ask a question..."):
    # 5.1 Add user message to history and show it
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 5.2 Show a "Thinking..." placeholder for the assistant
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")

        # 5.3 Call the chat service
        try:
            start_time = time.time()

            response = requests.post(
                CHAT_ENDPOINT,
                json={"query": query},
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
                answer = f"[Error: {error_detail}]"

        # 5.6 Handle network/connection errors
        except requests.exceptions.RequestException as e:
            placeholder.error(f"Could not reach the chat service: {e}")
            answer = f"[Error: {e}]"

    # 5.7 Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": answer})