from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AUTO - Digital Marketplace with AI",
    description="Automated marketplace for digital products with AI integration",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.endpoints import (
    users,
    products,
    orders,
    chat,
    ai_agent,
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(ai_agent.router, prefix="/api/ai", tags=["ai"])

@app.get("/")
async def root():
    return {"message": "Welcome to AUTO - Digital Marketplace with AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
