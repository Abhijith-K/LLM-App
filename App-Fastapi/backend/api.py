from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.ollama_utils import generate_from_ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, open CORS
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "👋 Hello from FastAPI"}

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(data: PromptRequest):
    result = generate_from_ollama(data.prompt)
    return {"response": result}
