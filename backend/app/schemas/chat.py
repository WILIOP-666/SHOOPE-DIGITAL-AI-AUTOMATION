from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Chat Message
class ChatMessage(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

# Chat Response
class ChatResponse(BaseModel):
    message: str
