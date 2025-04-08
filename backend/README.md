# AUTO - Backend

This is the backend for the AUTO digital marketplace with AI integration.

## Features

- User authentication and authorization
- Product management
- Order processing
- AI agent for chat responses
- Vector database integration (Pinecone)
- Graph database integration (Neo4j)
- Shopee marketplace integration
- Digital product delivery system

## Setup

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment:
```
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=auto

# Vector Database (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=auto-faq

# Graph Database (Neo4j)
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Shopee Integration
SHOPEE_API_URL=https://partner.shopeemobile.com
SHOPEE_PARTNER_ID=your_shopee_partner_id
SHOPEE_PARTNER_KEY=your_shopee_partner_key
```

5. Initialize the database:
```
python init_db.py
```

6. Run the server:
```
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
