from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai_agent import AgentConfig, AgentResponse, FAQQuery
from app.services.vector_service import search_vector_database
from app.services.graph_service import store_memory, retrieve_memory

router = APIRouter()

@router.post("/configure", response_model=AgentResponse)
def configure_ai_agent(
    config: AgentConfig,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Configure AI agent settings.
    """
    # Implementation will be added
    pass

@router.get("/config", response_model=AgentConfig)
def get_ai_config(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get current AI agent configuration.
    """
    # Implementation will be added
    pass

@router.post("/faq", response_model=Dict[str, Any])
async def query_faq(
    query: FAQQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Query the FAQ system using vector search.
    """
    # Search vector database for similar questions
    results = await search_vector_database(query.question, threshold=0.75)
    
    # Store the interaction in graph database for long-term memory
    await store_memory(current_user.id, "faq_query", {"question": query.question, "results": results})
    
    return {"results": results}

@router.get("/memory/{user_id}", response_model=Dict[str, Any])
async def get_user_memory(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve user memory from graph database.
    """
    # Check permissions
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Retrieve memory from graph database
    memory = await retrieve_memory(user_id)
    return {"memory": memory}
