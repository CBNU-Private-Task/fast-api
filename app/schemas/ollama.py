from pydantic import BaseModel
from typing import Optional

class OllamaRequest(BaseModel):
    prompt: str
    write_to_file: Optional[bool] = True

class OllamaResponse(BaseModel):
    success: bool
    prompt: str
    response: dict
    ai_content: str
    file_written: bool
    vscode_trigger_result: Optional[dict] 