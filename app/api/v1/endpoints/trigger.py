from fastapi import APIRouter
from pydantic import BaseModel
from app.core.websocket_manager import manager

router = APIRouter()

class TriggerRequest(BaseModel):
    action: str
    user_id: int

@router.post("/triggers", summary="Send a trigger to a specific client")
async def trigger_action(request: TriggerRequest):
    """
    Receives a trigger action and sends it to a specific user's WebSocket client(s).
    """
    response_data = {"success": True, "message": f"Triggered: {request.action} for user {request.user_id}"}
    await manager.send_to_user(request.user_id, response_data)
    return {"status": f"Trigger sent to user {request.user_id}"}
