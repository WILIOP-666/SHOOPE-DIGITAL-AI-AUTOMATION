from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.models.ai_config import StoreLevel

# AI Agent Configuration
class AgentConfig(BaseModel):
    is_active: bool = True
    store_level: StoreLevel = StoreLevel.USER_ID
    faq_threshold: float = 0.75
    custom_prompt: Optional[str] = None

# AI Agent Response
class AgentResponse(BaseModel):
    success: bool
    message: str

# FAQ Query
class FAQQuery(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

# Chat Message
class ChatMessage(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None
