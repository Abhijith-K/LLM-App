import subprocess
import requests
import time
import platform
import shutil
import json
import ollama

def is_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except:
        return False

def start_ollama():
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        print("❌ 'ollama' not found in PATH. Please add it or provide full path.")
        return

    print(f"🔧 Starting Ollama using: {ollama_path}")
    
    subprocess.Popen(
        [ollama_path, "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for Ollama to boot
    for _ in range(20):
        if is_ollama_running():
            print("✅ Ollama started successfully.")
            return
        time.sleep(1)

    print("❌ Failed to start Ollama after 20 seconds.")



def generate_from_ollama(prompt: str, model: str = "gemma3"):
    """Send a prompt to the local Ollama model and return the response."""
    try:

        
        response = ollama.chat(model = model, messages=[{"role":"user", "content": prompt}])
        #return {"Response" : response["message"]["content"]}
        
        # Print the raw response text for debugging
        #print(f"🔍 Raw Response: {response.text}")
        
        # If the response is successful, try to parse the JSON response
        if response:
            
            return response["message"]["content"]
            
        else:
            return f"❌ Error: {response}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {e}"
