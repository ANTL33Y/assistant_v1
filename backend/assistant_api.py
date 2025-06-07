from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

class ChatMessage(BaseModel):
    id: str
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = []


def create_app(prod: bool = False) -> FastAPI:
    app = FastAPI()

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
        """Echo back the last user message from the list."""
        messages = payload.messages
        if messages:
            last = messages[-1].content
        else:
            last = ""
        return {"text": f"You said: {last}"}

    @app.post("/speech-to-text")
    async def speech_to_text(file: UploadFile = File(...)):
        # Stub transcription
        content = await file.read()
        length = len(content)
        return {"text": f"Received {length} bytes of audio"}

    return app

app = create_app(prod=os.getenv("ENV") == "prod")
