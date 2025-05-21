import streamlit as st

def chat_ui(send_prompt_callback):
    st.title("🧠 Chat with Ollama")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:", key="user_input")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = send_prompt_callback(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": response})

    for msg in st.session_state.chat_history:
        role = "🧍 You" if msg["role"] == "user" else "🤖 Bot"
        st.markdown(f"**{role}:** {msg['content']}")
