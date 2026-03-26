from fastapi import FastAPI
from llm import chat_with_llm
from llm import chat_with_llm_stream


from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory=".", html=True), name="static")



app = FastAPI()

# 🔥 加这个（允许跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 所有来源都允许（开发用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = []

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/chat")
def chat(q: str):
    global chat_history

    chat_history.append({"role": "user", "content": q})

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    answer = chat_with_llm(chat_history)

    chat_history.append({"role": "assistant", "content": answer})

    return {"answer": answer}

@app.get("/chat_stream")
def chat_stream(q: str):
    global chat_history

    chat_history.append({"role": "user", "content": q})

    def generate():
        answer = ""
        for chunk in chat_with_llm_stream(chat_history):
            answer += chunk
            yield chunk

        chat_history.append({"role": "assistant", "content": answer})
    return StreamingResponse(generate(), media_type="text/plain")

import os

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
