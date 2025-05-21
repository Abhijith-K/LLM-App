import streamlit as st
import requests

st.set_page_config(page_title="Gemma with Ollama", layout="wide")
st.title("🧠 Gemma with Ollama - Interactive Prompting")

# Sidebar for parameter controls
st.sidebar.header("Generation Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
top_k = st.sidebar.slider("Top-k", 0, 100, 40)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.9)
min_p = st.sidebar.slider("Min-p", 0.0, 1.0, 0.05)
model_name = st.sidebar.text_input("Model name", "gemma:3")

# Main interface
prompt = st.text_area("Enter your prompt", height=200)
generate_button = st.button("Generate")

# Generate response
if generate_button and prompt.strip():
    with st.spinner("Generating response..."):
        try:
            response = requests.post(
                "http://localhost:8000/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "options": {
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "min_p": min_p
                    },
                    "stream": False
                }
            )
            result = response.json()
            st.markdown("### 🔍 Response:")
            st.write(result["response"])
        except Exception as e:
            st.error(f"Error: {e}")
