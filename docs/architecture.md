# AUTO System Architecture

This document outlines the architecture of the AUTO digital marketplace system.

## System Overview

AUTO is a comprehensive platform for selling and delivering digital products with AI-powered automation. The system consists of three main components:

1. **Backend API**: Handles business logic, database operations, and AI processing
2. **Frontend Web Application**: Provides user interface for managing products, orders, and AI settings
3. **Browser Extension**: Integrates with Shopee marketplace for order monitoring and product delivery

## Component Architecture

### Backend (FastAPI)

The backend is built with FastAPI and follows a modular architecture:

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/       # API route handlers
│   ├── core/                # Core functionality and config
│   ├── db/                  # Database models and session
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic services
└── main.py                  # Application entry point
```

#### Key Components:

1. **API Layer**: RESTful endpoints for user, product, order, and AI operations
2. **Database Layer**: SQLAlchemy models and database session management
3. **Service Layer**: Business logic for product delivery, AI processing, etc.
4. **Integration Layer**: Connections to external services (Pinecone, Neo4j, Shopee)

### Frontend (Next.js)

The frontend is built with Next.js and follows a modern React architecture:

```
frontend/
├── src/
│   ├── app/                 # Next.js app router pages
│   ├── components/          # React components
│   ├── lib/                 # Utility functions
│   └── services/            # API service clients
└── public/                  # Static assets
```

#### Key Components:

1. **Pages**: Next.js pages for different sections of the application
2. **Components**: Reusable UI components
3. **Services**: API clients for communicating with the backend
4. **State Management**: React hooks and context for state management

### Browser Extension (Plasmo)

The browser extension is built with Plasmo and follows a standard extension architecture:

```
extension/
└── auto-extension/
    ├── popup.tsx            # Extension popup UI
    ├── background.ts        # Background script
    └── content.ts           # Content script for Shopee integration
```

#### Key Components:

1. **Popup UI**: User interface for the extension popup
2. **Background Script**: Handles API communication and notifications
3. **Content Script**: Integrates with Shopee pages for order detection and processing

## Data Flow

1. **Order Creation**:
   - Customer places an order on Shopee
   - Extension detects the order and sends it to the backend
   - Backend creates an order record in the database

2. **Order Processing**:
   - Backend checks order status periodically
   - When payment is confirmed, the order status is updated to "PAID"

3. **Product Delivery**:
   - Backend delivers the digital product based on product type
   - Order status is updated to "DELIVERED"
   - Customer receives the digital product

4. **AI Interaction**:
   - Customer sends a message through the chat interface
   - Backend processes the message using vector search for FAQ matching
   - If a match is found, the answer is returned directly
   - If no match is found, the AI generates a response
   - Interaction is stored in the graph database for future reference

## Technology Stack

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

## Deployment Architecture

The system can be deployed using the following architecture:

1. **Backend**: Deployed on a cloud server (e.g., AWS, GCP, Azure)
2. **Frontend**: Deployed as a static site on a CDN (e.g., Vercel, Netlify)
3. **Database**: Hosted database services (e.g., PostgreSQL on RDS)
4. **Vector Database**: Pinecone cloud service
5. **Graph Database**: Neo4j cloud service or self-hosted
6. **Extension**: Distributed through browser extension stores
