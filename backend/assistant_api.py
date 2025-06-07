from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os
import openai
from src.config import Settings

class ChatMessage(BaseModel):
    id: str
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = []


def create_app(prod: bool = False) -> FastAPI:
    app = FastAPI()
    cfg = Settings.load()
    client = openai.OpenAI(api_key=cfg.openai_api_key) if cfg.openai_api_key else None

    if prod:
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        if os.path.isdir(static_dir):
            app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    else:
        # Allow front-end dev server
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.post("/chat")
    async def chat(payload: ChatRequest):
        """Send the chat transcript to OpenAI and return the assistant reply."""
        if client is None:
            messages = payload.messages
            last = messages[-1].content if messages else ""
            return {"text": f"You said: {last}"}
        chat_messages = [
            {"role": m.role, "content": m.content} for m in payload.messages
        ]
        resp = client.chat.completions.create(
            model=cfg.openai_model_name, messages=chat_messages
        )
        text = resp.choices[0].message.content.strip()
        return {"text": text}

    @app.post("/speech-to-text")
    async def speech_to_text(file: UploadFile = File(...)):
        # Stub transcription
        content = await file.read()
        length = len(content)
        return {"text": f"Received {length} bytes of audio"}

    return app

app = create_app(prod=os.getenv("ENV") == "prod")
