from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI()
app.context = []


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # The origin of your frontend app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat_with_ollama(request: ChatRequest):
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "aya:latest",
        "prompt": request.message,
        "stream": False,
        "context": app.context
    }

    print(request.message)

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(ollama_url, json=payload, headers=headers)
    text = response.text
    if response.status_code != 200:
        print(text)
        return "error in getting request"
    
    print("The response from the model is:", text)
    data = json.loads(text)
    if "context" in data:
        app.context = data["context"]
    return data["response"]
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)