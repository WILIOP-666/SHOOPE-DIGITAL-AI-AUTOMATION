import os
from typing import List, Dict, Any, Optional
import pinecone
from app.core.config import settings

# Initialize Pinecone
def init_pinecone():
    """Initialize Pinecone client."""
    if not settings.PINECONE_API_KEY or not settings.PINECONE_ENVIRONMENT:
        raise ValueError("Pinecone API key and environment must be set")
    
    pinecone.init(
        api_key=settings.PINECONE_API_KEY,
        environment=settings.PINECONE_ENVIRONMENT
    )
    
    # Check if index exists, if not create it
    if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=1536,  # OpenAI embeddings dimension
            metric="cosine"
        )
    
    return pinecone.Index(settings.PINECONE_INDEX_NAME)

# Get embeddings for text
async def get_embeddings(text: str) -> List[float]:
    """
    Get embeddings for text using OpenAI's embedding model.
    This is a placeholder - in a real implementation, you would use the OpenAI API.
    """
    # Placeholder for embeddings
    return [0.0] * 1536  # Return a vector of zeros with dimension 1536

# Search vector database
async def search_vector_database(query: str, threshold: float = 0.75, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search the vector database for similar questions.
    """
    try:
        # Get embeddings for the query
        query_embedding = await get_embeddings(query)
        
        # Initialize Pinecone
        index = init_pinecone()
        
        # Search Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        formatted_results = []
        for match in results.matches:
            if match.score >= threshold:
                formatted_results.append({
                    "question": match.metadata.get("question", ""),
                    "answer": match.metadata.get("answer", ""),
                    "score": match.score
                })
        
        return formatted_results
    except Exception as e:
        print(f"Error searching vector database: {e}")
        # For development, return mock data
        return [
            {
                "question": "How do I reset my password?",
                "answer": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
                "score": 0.95
            },
            {
                "question": "How do I contact support?",
                "answer": "You can contact support by sending an email to support@example.com or by using the contact form on our website.",
                "score": 0.85
            }
        ]

# Store FAQ in vector database
async def store_faq(question: str, answer: str) -> bool:
    """
    Store a FAQ in the vector database.
    """
    try:
        # Get embeddings for the question
        question_embedding = await get_embeddings(question)
        
        # Initialize Pinecone
        index = init_pinecone()
        
        # Store in Pinecone
        index.upsert(
            vectors=[
                {
                    "id": f"faq_{hash(question)}",
                    "values": question_embedding,
                    "metadata": {
                        "question": question,
                        "answer": answer
                    }
                }
            ]
        )
        
        return True
    except Exception as e:
        print(f"Error storing FAQ in vector database: {e}")
        return False
