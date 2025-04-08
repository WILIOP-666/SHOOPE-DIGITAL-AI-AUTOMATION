import os
import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.ai_config import AIConfig, StoreLevel
from app.services.vector_service import search_vector_database
from app.services.graph_service import store_memory, retrieve_memory

async def process_chat_message(message: str, user_id: int, db: Session) -> str:
    """
    Process a chat message with AI and return a response.
    """
    # Get user's AI configuration
    ai_config = db.query(AIConfig).filter(AIConfig.user_id == user_id).first()
    
    if not ai_config or not ai_config.is_active:
        return "AI assistant is not active for this user."
    
    # Check if we have a relevant FAQ answer
    faq_results = await search_vector_database(message, threshold=ai_config.faq_threshold)
    
    if faq_results and len(faq_results) > 0 and faq_results[0]["score"] >= ai_config.faq_threshold:
        # Store the interaction in memory
        await store_memory(
            user_id=user_id,
            interaction_type="faq_response",
            data={
                "query": message,
                "response": faq_results[0]["answer"],
                "score": faq_results[0]["score"]
            }
        )
        return faq_results[0]["answer"]
    
    # If no FAQ match, use OpenAI for a response
    # This is a placeholder - in a real implementation, you would use the OpenAI API
    response = f"I understand you're asking about: {message}. Let me help you with that."
    
    # Store the interaction in memory
    await store_memory(
        user_id=user_id,
        interaction_type="ai_response",
        data={
            "query": message,
            "response": response
        }
    )
    
    return response

async def check_ai_enabled(user_id: int, product_id: Optional[int] = None, db: Session = None) -> bool:
    """
    Check if AI is enabled for a user or product.
    """
    if not db:
        return False
        
    # Get user's AI configuration
    ai_config = db.query(AIConfig).filter(AIConfig.user_id == user_id).first()
    
    if not ai_config or not ai_config.is_active:
        return False
    
    # Check based on store level
    if ai_config.store_level == StoreLevel.STORE:
        return True
    elif ai_config.store_level == StoreLevel.USER_ID:
        return True
    elif ai_config.store_level == StoreLevel.PRODUCT and product_id:
        # Check if AI is enabled for this specific product
        product = db.query(Product).filter(Product.id == product_id).first()
        return product and product.ai_enabled
    
    return False
