import os
import json
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jService:
    def __init__(self):
        self.uri = settings.NEO4J_URI
        self.username = settings.NEO4J_USERNAME
        self.password = settings.NEO4J_PASSWORD
        self.driver = None
        
    def connect(self):
        """Connect to Neo4j database."""
        if not self.driver:
            try:
                self.driver = GraphDatabase.driver(
                    self.uri, 
                    auth=(self.username, self.password)
                )
            except Exception as e:
                print(f"Failed to connect to Neo4j: {e}")
                # For development, we'll continue without failing
                pass
    
    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
            
    def run_query(self, query, parameters=None):
        """Run a Cypher query."""
        if not self.driver:
            self.connect()
            
        if not self.driver:
            # If still no driver, we're in development mode
            print(f"Development mode: would run query: {query}")
            return []
            
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Initialize Neo4j service
neo4j_service = Neo4jService()

async def store_memory(user_id: int, interaction_type: str, data: Dict[str, Any]) -> bool:
    """
    Store a memory in the graph database.
    """
    try:
        # Convert data to JSON string
        data_json = json.dumps(data)
        
        # Create query
        query = """
        MERGE (u:User {id: $user_id})
        CREATE (m:Memory {
            id: randomUUID(),
            type: $type,
            data: $data,
            timestamp: datetime()
        })
        CREATE (u)-[:HAS_MEMORY]->(m)
        RETURN m
        """
        
        # Run query
        neo4j_service.run_query(query, {
            "user_id": user_id,
            "type": interaction_type,
            "data": data_json
        })
        
        return True
    except Exception as e:
        print(f"Error storing memory in graph database: {e}")
        return False

async def retrieve_memory(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve memories for a user from the graph database.
    """
    try:
        # Create query
        query = """
        MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
        RETURN m.id as id, m.type as type, m.data as data, m.timestamp as timestamp
        ORDER BY m.timestamp DESC
        LIMIT $limit
        """
        
        # Run query
        results = neo4j_service.run_query(query, {
            "user_id": user_id,
            "limit": limit
        })
        
        # Format results
        memories = []
        for record in results:
            try:
                data = json.loads(record["data"])
            except:
                data = {}
                
            memories.append({
                "id": record["id"],
                "type": record["type"],
                "data": data,
                "timestamp": record["timestamp"]
            })
        
        return memories
    except Exception as e:
        print(f"Error retrieving memory from graph database: {e}")
        # For development, return mock data
        return [
            {
                "id": "1",
                "type": "faq_response",
                "data": {
                    "query": "How do I reset my password?",
                    "response": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
                    "score": 0.95
                },
                "timestamp": "2023-04-01T12:00:00Z"
            },
            {
                "id": "2",
                "type": "ai_response",
                "data": {
                    "query": "Tell me about your digital products",
                    "response": "We offer various digital products including templates, accounts, links, and vouchers."
                },
                "timestamp": "2023-04-01T12:05:00Z"
            }
        ]
