# AI Integration Guide

This document explains how the AI components are integrated into the AUTO marketplace system.

## Overview

AUTO uses AI for several key features:

1. **Automated Chat Responses**: AI responds to customer inquiries automatically
2. **FAQ Matching**: Vector search to find relevant answers to common questions
3. **Long-term Memory**: Graph database to store and retrieve customer interactions
4. **Personalization**: Tailoring responses based on user history and preferences

## Components

### Vector Database (Pinecone)

The vector database stores embeddings of FAQ questions and answers, allowing for semantic search.

#### How it works:

1. FAQ questions and answers are converted to vector embeddings using OpenAI's embedding model
2. These embeddings are stored in Pinecone with metadata (question, answer)
3. When a user asks a question, it's converted to an embedding and compared to stored embeddings
4. If a match above the threshold is found, the corresponding answer is returned

#### Implementation:

```python
# Convert text to embedding
async def get_embeddings(text: str) -> List[float]:
    # In a real implementation, call OpenAI API
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Search for similar questions
async def search_vector_database(query: str, threshold: float = 0.75) -> List[Dict]:
    query_embedding = await get_embeddings(query)
    
    # Search Pinecone
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )
    
    # Filter by threshold
    filtered_results = [
        {
            "question": match.metadata["question"],
            "answer": match.metadata["answer"],
            "score": match.score
        }
        for match in results.matches
        if match.score >= threshold
    ]
    
    return filtered_results
```

### Graph Database (Neo4j)

The graph database stores user interactions and relationships, creating a knowledge graph for long-term memory.

#### How it works:

1. User interactions (questions, responses) are stored as nodes in the graph
2. Relationships between users, questions, and products are established
3. This creates a knowledge graph that can be queried for context
4. The AI can use this context to provide more personalized responses

#### Implementation:

```python
# Store a memory in the graph
async def store_memory(user_id: int, interaction_type: str, data: Dict) -> bool:
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
    
    neo4j_session.run(query, {
        "user_id": user_id,
        "type": interaction_type,
        "data": json.dumps(data)
    })
    
    return True

# Retrieve memories for a user
async def retrieve_memory(user_id: int, limit: int = 10) -> List[Dict]:
    query = """
    MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
    RETURN m.id as id, m.type as type, m.data as data, m.timestamp as timestamp
    ORDER BY m.timestamp DESC
    LIMIT $limit
    """
    
    results = neo4j_session.run(query, {
        "user_id": user_id,
        "limit": limit
    })
    
    memories = []
    for record in results:
        memories.append({
            "id": record["id"],
            "type": record["type"],
            "data": json.loads(record["data"]),
            "timestamp": record["timestamp"]
        })
    
    return memories
```

### AI Chat Service

The AI chat service processes user messages and generates responses.

#### How it works:

1. User sends a message through the chat interface
2. The system checks if there's a matching FAQ in the vector database
3. If a match is found, the answer is returned directly
4. If no match is found, the system retrieves context from the graph database
5. The context and message are sent to the OpenAI API for a response
6. The interaction is stored in the graph database for future reference

#### Implementation:

```python
async def process_chat_message(message: str, user_id: int, db: Session) -> str:
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
    
    # If no FAQ match, retrieve context from memory
    memories = await retrieve_memory(user_id)
    
    # Format context for OpenAI
    context = format_context_from_memories(memories)
    
    # Call OpenAI API with context
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ai_config.custom_prompt or "You are a helpful assistant."},
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": message}
        ]
    )
    
    ai_response = response.choices[0].message.content
    
    # Store the interaction in memory
    await store_memory(
        user_id=user_id,
        interaction_type="ai_response",
        data={
            "query": message,
            "response": ai_response
        }
    )
    
    return ai_response
```

## Configuration Options

The AI system can be configured at different levels:

### Store Level

AI is enabled for all products and users in the store.

### Product Level

AI is enabled only for specific products.

### User Level

AI is enabled only for specific users.

### Configuration Parameters

- `is_active`: Whether AI is enabled
- `store_level`: The level at which AI is enabled (store, product, user_id)
- `faq_threshold`: The similarity threshold for FAQ matching (0.0 to 1.0)
- `custom_prompt`: A custom system prompt for the AI

## Training the AI

### FAQ Training

To add new FAQs to the vector database:

1. Create a list of question-answer pairs
2. Convert questions to embeddings
3. Store embeddings and metadata in Pinecone

Example:

```python
async def add_faq(question: str, answer: str) -> bool:
    # Convert question to embedding
    embedding = await get_embeddings(question)
    
    # Store in Pinecone
    pinecone_index.upsert(
        vectors=[
            {
                "id": f"faq_{hash(question)}",
                "values": embedding,
                "metadata": {
                    "question": question,
                    "answer": answer
                }
            }
        ]
    )
    
    return True
```

### Custom Prompts

You can customize the AI's behavior by setting a custom system prompt:

```python
async def set_custom_prompt(user_id: int, prompt: str, db: Session) -> bool:
    ai_config = db.query(AIConfig).filter(AIConfig.user_id == user_id).first()
    
    if not ai_config:
        ai_config = AIConfig(user_id=user_id)
        db.add(ai_config)
    
    ai_config.custom_prompt = prompt
    db.commit()
    
    return True
```

## Best Practices

1. **Start with a good set of FAQs**: The more comprehensive your FAQ database, the more questions can be answered without calling the OpenAI API.

2. **Set an appropriate threshold**: A threshold that's too low will return incorrect answers, while a threshold that's too high will miss relevant answers.

3. **Use custom prompts**: Tailor the AI's behavior to your specific use case with custom prompts.

4. **Monitor and improve**: Regularly review AI responses and add new FAQs based on common questions.

5. **Consider privacy**: Be mindful of what information is stored in the graph database and ensure compliance with privacy regulations.
