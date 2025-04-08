from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.ai_service import process_chat_message

router = APIRouter()

@router.post("/send", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Send a chat message and get AI response.
    """
    # Process the message with AI
    response = await process_chat_message(message.content, current_user.id, db)
    return {"message": response}

# WebSocket connection for real-time chat
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db),
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process the message with AI
            response = await process_chat_message(data, user_id, db)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        # Handle disconnect
        pass
