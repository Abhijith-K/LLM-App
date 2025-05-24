import requests

def is_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        return True
    except:
        return False

def generate_response(prompt, model, temperature):

    if is_ollama_running():

        url = "http://localhost:11434/api/generate"
        payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()
            if "response" in data:
                return data["response"]
            else:
                raise ValueError("Unexpected response format: 'response' key not found")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the API: {e}")
            return None
        except ValueError as e:
            print(f"Error processing the API response: {e}")
            return None
  
    else:

        return "Ollama is not running. Please start it first."
    