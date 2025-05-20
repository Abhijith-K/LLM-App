import streamlit as st
import requests

st.set_page_config(page_title="Ollama Generator")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Start"])

if page == "Home":
    try:
        response = requests.get("http://localhost:8000/")
        st.write(response.json()["message"])
    except:
        st.error("Backend not reachable.")

if page == "Start":
    prompt = st.text_area("Enter your prompt:")
    if st.button("Generate"):
        with st.spinner("Generating..."):
            try:
                res = requests.post("http://localhost:8000/generate", json={"prompt": prompt})
                if res.ok:
                    st.success(res.json()["response"])
                else:
                    st.error("Backend error.")
            except:
                st.error("Failed to contact API.")
