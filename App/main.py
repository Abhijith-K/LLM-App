import time
import threading
import subprocess
import sys
import webbrowser
from backend.ollama_utils import is_ollama_running, start_ollama

# === Start Ollama ===
if not is_ollama_running():
    print("🔄 Starting Ollama...")
    start_ollama()
    time.sleep(5)
else:
    print("✅ Ollama is already running.")

# === Start FastAPI ===
def start_fastapi():
    subprocess.run([sys.executable, "-m", "uvicorn", "backend.api:app", "--port", "8000"])

# === Start Streamlit ===
def start_streamlit():
    url = "http://localhost:8501"
    print(f"🚀 Opening Streamlit app at {url}")
    webbrowser.open_new_tab(url)  # ⬅️ Open the UI in default browser
    subprocess.run([
        "streamlit", "run", "frontend/ui.py",
        "--server.headless", "true",  # ensure it runs without CLI interaction
        "--browser.serverAddress", "localhost"
    ])

# === Run both services ===
threading.Thread(target=start_fastapi, daemon=True).start()
time.sleep(2)
start_streamlit()
