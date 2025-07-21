from fastapi import APIRouter
from .endpoints import ollama, article, auth, trigger, websocket

api_router = APIRouter()

api_router.include_router(ollama.router, tags=["ollama"]) 
api_router.include_router(article.router, tags=["articles"])
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(trigger.router, tags=["triggers"])
api_router.include_router(websocket.router, tags=["websocket"])