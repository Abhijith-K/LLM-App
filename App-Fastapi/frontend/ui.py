import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Gemma Chat", layout="wide")
st.title("🧠 Chat with Gemma (via Ollama)")

# Constants
CHAT_HISTORY_FILE = "chat_history.json"
MAX_TURNS = 6  # Number of (user + assistant) pairs to keep in context

# Load chat history
if "chat_history" not in st.session_state:
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            st.session_state.chat_history = json.load(f)
    else:
        st.session_state.chat_history = []

# Sidebar - generation parameters
st.sidebar.header("Generation Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
top_k = st.sidebar.slider("Top-k", 0, 100, 40)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.9)
min_p = st.sidebar.slider("Min-p", 0.0, 1.0, 0.05)
model_name = st.sidebar.text_input("Model name", "gemma:2b")

st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)
    st.rerun()

if st.sidebar.button("💾 Save Chat"):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(st.session_state.chat_history, f, indent=2)
    st.sidebar.success("Chat saved!")

# Display chat history (at top)
st.markdown("### 💬 Chat History")
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f"**🧍 You:** {content}")
    else:
        st.markdown(f"**🤖 Gemma:** {content}")

st.markdown("---")

# Chat input form (at bottom)
st.markdown("### ✍️ Type your message")
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        prompt = st.text_input("Your message:", label_visibility="collapsed", placeholder="Ask Gemma something...", key="user_input")
    with col2:
        submitted = st.form_submit_button("Send")

# Handle input
if submitted and prompt.strip():
    # Save user input to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Get last few messages for context
    recent_history = st.session_state.chat_history[-MAX_TURNS * 2:]

    # Construct the prompt with chat history
    chat_context = ""
    for msg in recent_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        chat_context += f"{role}: {msg['content']}\n"
    chat_context += f"User: {prompt}\nAssistant:"

    # Placeholder for streaming
    placeholder = st.empty()
    full_response = ""

    with st.spinner("Gemma is thinking..."):
        try:
            response = requests.post(
                "http://localhost:8000/generate",
                json={
                    "model": model_name,
                    "prompt": chat_context,
                    "options": {
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "min_p": min_p
                    },
                    "stream": True
                },
                stream=True
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    full_response += token
                    placeholder.markdown(f"**🤖 Gemma:** {full_response}")

        except Exception as e:
            full_response = f"⚠️ Error: {e}"
            placeholder.markdown(full_response)

    # Save assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# Scroll to bottom on submit
st.markdown("""<script>window.scrollTo(0, document.body.scrollHeight);</script>""", unsafe_allow_html=True)

# Add space at the bottom to keep input visually anchored
st.markdown("<br><br><br>", unsafe_allow_html=True)
