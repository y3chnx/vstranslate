import uvicorn
import os
import webbrowser
from threading import Timer
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from llama_cpp import Llama

app = FastAPI()

# Models
llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",
    filename="qwen2.5-coder-7b-instruct-q3_k_m.gguf",
)

# HTML frontend
@app.get("/")
async def read_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(index_path)

@app.get("/icon.png")
async def get_icon():
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    return FileResponse(icon_path)

# Chatting funcs
@app.post("/chat")
async def chat_endpoint(request: Request):
    # Manually parse the JSON body
    data = await request.json()
    incoming_messages = data.get("messages", [])
    
    # Prompting
    system_prompt = {"role": "system", "content": "You are a professional programming language translator. Translate the provided code strictly into the target language requested. The output of the code that you translated, and code that you asked for translate should be exactly same. Output ONLY the translated code. Do not provide explanations, and do not use markdown backticks unless they are part of the code, and do not talk back."}
    
    response = llm.create_chat_completion(messages=[system_prompt] + incoming_messages)
    return response

if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000")).start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)