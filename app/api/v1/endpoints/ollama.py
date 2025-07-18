from fastapi import APIRouter
from ....schemas.ollama import OllamaRequest, OllamaResponse
from ....services.ollama import call_ollama_service

router = APIRouter()

@router.post("/ollama", response_model=OllamaResponse)
def call_ollama(request: OllamaRequest):
    write_to_file = request.write_to_file if request.write_to_file is not None else True
    return call_ollama_service(request.prompt, write_to_file)