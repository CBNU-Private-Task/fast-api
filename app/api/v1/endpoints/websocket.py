from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from app.core.websocket_manager import manager
from app.core.Oauth import verify_token
from app.schemas.auth import DataToken

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    The authenticated WebSocket endpoint for clients.
    A valid JWT token must be provided as a query parameter.
    Example: ws://localhost:8000/api/v1/ws?token=YOUR_JWT_TOKEN
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    try:
        token_data: DataToken = verify_token(token, credentials_exception)
        user_id = token_data.id
        if user_id is None:
            raise credentials_exception
            
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket) 