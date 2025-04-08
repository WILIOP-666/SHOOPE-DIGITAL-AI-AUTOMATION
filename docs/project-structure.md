# AUTO Project Structure

This document provides an overview of the AUTO project structure.

## Main Directories

```
AUTO/
├── backend/             # FastAPI backend
├── frontend/            # Next.js frontend
├── extension/           # Plasmo browser extension
└── docs/                # Documentation
```

## Backend Structure

```
backend/
├── app/                 # Application code
│   ├── api/             # API endpoints
│   │   └── endpoints/   # API route handlers
│   ├── core/            # Core functionality
│   ├── db/              # Database models and session
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic services
├── main.py              # Application entry point
├── init_db.py           # Database initialization script
├── requirements.txt     # Python dependencies
└── README.md            # Backend documentation
```

### Key Backend Files

- `app/main.py`: FastAPI application entry point
- `app/api/endpoints/`: API route handlers for users, products, orders, chat, and AI
- `app/core/config.py`: Application configuration
- `app/core/security.py`: Authentication and security
- `app/db/session.py`: Database session management
- `app/models/`: SQLAlchemy models for database tables
- `app/schemas/`: Pydantic schemas for request/response validation
- `app/services/`: Business logic services

## Frontend Structure

```
frontend/
├── src/                 # Source code
│   ├── app/             # Next.js app router pages
│   │   ├── auth/        # Authentication pages
│   │   └── dashboard/   # Dashboard pages
│   ├── components/      # React components
│   │   ├── chat/        # Chat components
│   │   ├── layout/      # Layout components
│   │   ├── orders/      # Order components
│   │   ├── products/    # Product components
│   │   └── ui/          # UI components
│   ├── lib/             # Utility functions
│   └── services/        # API service clients
├── public/              # Static assets
├── package.json         # Node.js dependencies
└── README.md            # Frontend documentation
```

### Key Frontend Files

- `src/app/page.tsx`: Home page
- `src/app/auth/login/page.tsx`: Login page
- `src/app/auth/register/page.tsx`: Registration page
- `src/app/dashboard/page.tsx`: Dashboard page
- `src/app/dashboard/products/page.tsx`: Products management page
- `src/app/dashboard/orders/page.tsx`: Orders management page
- `src/app/dashboard/chat/page.tsx`: AI chat interface
- `src/components/layout/DashboardLayout.tsx`: Dashboard layout
- `src/services/api.ts`: API client
- `src/services/auth.ts`: Authentication service
- `src/services/products.ts`: Products service
- `src/services/orders.ts`: Orders service
- `src/services/chat.ts`: Chat service

## Browser Extension Structure

```
extension/
└── auto-extension/      # Plasmo extension
    ├── popup.tsx        # Extension popup UI
    ├── background.ts    # Background script
    ├── content.ts       # Content script for Shopee integration
    ├── package.json     # Node.js dependencies
    └── README.md        # Extension documentation
```

### Key Extension Files

- `popup.tsx`: Extension popup UI
- `background.ts`: Background script for API communication and notifications
- `content.ts`: Content script for Shopee integration

## Documentation Structure

```
docs/
├── index.md             # Documentation index
├── architecture.md      # System architecture
├── api.md               # API documentation
├── ai-integration.md    # AI integration guide
└── project-structure.md # Project structure overview
```
