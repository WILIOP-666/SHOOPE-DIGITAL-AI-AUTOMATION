# AUTO - Digital Marketplace with AI

A complete digital marketplace solution with AI-powered automation, Shopee integration, and automatic product delivery.

## Project Overview

AUTO is a comprehensive platform for selling and delivering digital products with AI-powered automation. It consists of three main components:

1. **Backend (FastAPI)**: Handles API requests, database operations, AI processing, and product delivery
2. **Frontend (Next.js)**: Provides user interface for managing products, orders, and AI settings
3. **Browser Extension (Plasmo)**: Integrates with Shopee marketplace for order monitoring and product delivery

## Features

### Core Features
- User authentication and authorization
- Product management (templates, accounts, links, vouchers)
- Order processing and tracking
- Digital product delivery automation
- Shopee marketplace integration

### AI Features
- AI-powered chat responses for customer inquiries
- Vector database (Pinecone) for accurate FAQ responses
- Graph database (Neo4j) for long-term memory
- Configurable AI settings at store, product, and user levels

## Project Structure

- `backend/`: Python FastAPI backend
- `frontend/`: Next.js frontend
- `extension/`: Plasmo browser extension
- `docs/`: Documentation

## Documentation

- [Project Overview](docs/index.md)
- [System Architecture](docs/architecture.md)
- [API Documentation](docs/api.md)
- [AI Integration Guide](docs/ai-integration.md)
- [Project Structure](docs/project-structure.md)
- [Project Summary](docs/summary.md)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```
cd backend
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
```
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Create a `.env` file with the necessary environment variables (see `backend/README.md` for details)

6. Initialize the database:
```
python init_db.py
```

7. Run the server:
```
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Create a `.env.local` file with the necessary environment variables (see `frontend/README.md` for details)

4. Run the development server:
```
npm run dev
```

### Browser Extension Setup

1. Navigate to the extension directory:
```
cd extension/auto-extension
```

2. Install dependencies:
```
npm install
```

3. Run the development server:
```
npm run dev
```

4. Load the extension in your browser (see `extension/auto-extension/README.md` for details)

## Technologies Used

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy
- Pinecone (Vector Database)
- Neo4j (Graph Database)
- OpenAI API

### Frontend
- Next.js 14
- React 19
- TypeScript
- Tailwind CSS

### Browser Extension
- Plasmo
- React
- TypeScript

## License

This project is licensed under the MIT License - see the LICENSE file for details.
