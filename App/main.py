import streamlit as st
from backend import generate_response
from frontend import chat_ui

def main():
    chat_ui(generate_response)

if __name__ == "__main__":
    main()
