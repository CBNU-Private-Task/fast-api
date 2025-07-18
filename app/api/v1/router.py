from fastapi import APIRouter
from .endpoints import ollama, article, auth

api_router = APIRouter()

api_router.include_router(ollama.router, tags=["ollama"]) 
api_router.include_router(article.router, tags=["articles"])
api_router.include_router(auth.router, tags=["authentication"])