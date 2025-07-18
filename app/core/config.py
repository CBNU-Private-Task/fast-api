import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://ollama.ksga.info/api/chat")
    VSCODE_SERVER_CONFIG_DIR: str = os.path.expanduser("~/.vscode-streaming-extension")

settings = Settings() 