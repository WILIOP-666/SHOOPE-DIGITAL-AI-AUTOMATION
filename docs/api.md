# AUTO API Documentation

This document provides information about the AUTO API endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Most API endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

To obtain a token, use the login endpoint.

## Endpoints

### Authentication

#### Login

```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "User Name",
    "is_active": true,
    "is_admin": false,
    "created_at": "2023-04-01T12:00:00Z",
    "updated_at": "2023-04-01T12:00:00Z"
  }
}
```

#### Register

```
POST /api/auth/register
```

Request body:
```json
{
  "email": "newuser@example.com",
  "password": "password",
  "full_name": "New User"
}
```

Response: Same as login endpoint

### Users

#### Get Current User

```
GET /api/users/me
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "is_admin": false,
  "created_at": "2023-04-01T12:00:00Z",
  "updated_at": "2023-04-01T12:00:00Z"
}
```

#### Update Current User

```
PUT /api/users/me
```

Request body:
```json
{
  "full_name": "Updated Name",
  "password": "new_password"  // Optional
}
```

Response: Updated user object

### Products

#### List Products

```
GET /api/products
```

Query parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)

Response:
```json
[
  {
    "id": 1,
    "name": "Digital Template",
    "description": "A digital template for your business",
    "price": 29.99,
    "product_type": "template",
    "content": "Template content here...",
    "is_active": true,
    "ai_enabled": false,
    "owner_id": 1,
    "created_at": "2023-04-01T12:00:00Z",
    "updated_at": "2023-04-01T12:00:00Z"
  },
  // More products...
]
```

#### Get Product

```
GET /api/products/{product_id}
```

Response: Product object

#### Create Product

```
POST /api/products
```

Request body:
```json
{
  "name": "New Product",
  "description": "Product description",
  "price": 19.99,
  "product_type": "template",
  "content": "Product content here...",
  "is_active": true,
  "ai_enabled": false
}
```

Response: Created product object

#### Update Product

```
PUT /api/products/{product_id}
```

Request body: Same as create product (all fields optional)

Response: Updated product object

#### Delete Product

```
DELETE /api/products/{product_id}
```

Response: No content (204)

### Orders

#### List Orders

```
GET /api/orders
```

Query parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)

Response:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "product_id": 1,
    "quantity": 1,
    "total_price": 29.99,
    "status": "paid",
    "shopee_order_id": "SHP123456",
    "delivery_data": "{}",
    "is_delivered": false,
    "created_at": "2023-04-01T12:00:00Z",
    "updated_at": "2023-04-01T12:00:00Z"
  },
  // More orders...
]
```

#### Get Order

```
GET /api/orders/{order_id}
```

Response: Order object

#### Create Order

```
POST /api/orders
```

Request body:
```json
{
  "product_id": 1,
  "quantity": 1,
  "total_price": 29.99,
  "shopee_order_id": "SHP123456"
}
```

Response: Created order object

#### Update Order

```
PUT /api/orders/{order_id}
```

Request body:
```json
{
  "status": "paid",
  "is_delivered": false
}
```

Response: Updated order object

#### Deliver Digital Product

```
POST /api/orders/{order_id}/deliver
```

Response: Updated order object with delivery information

### Chat

#### Send Message

```
POST /api/chat/send
```

Request body:
```json
{
  "content": "How do I use the template?",
  "metadata": {
    "product_id": 1
  }
}
```

Response:
```json
{
  "message": "To use the template, open it in your preferred software and customize the content according to your needs."
}
```

### AI Agent

#### Get AI Configuration

```
GET /api/ai/config
```

Response:
```json
{
  "is_active": true,
  "store_level": "user_id",
  "faq_threshold": 0.75,
  "custom_prompt": "You are a helpful assistant for AUTO marketplace."
}
```

#### Configure AI Agent

```
POST /api/ai/configure
```

Request body:
```json
{
  "is_active": true,
  "store_level": "user_id",
  "faq_threshold": 0.8,
  "custom_prompt": "You are a helpful assistant for AUTO marketplace."
}
```

Response:
```json
{
  "success": true,
  "message": "AI agent configured successfully"
}
```

#### Query FAQ

```
POST /api/ai/faq
```

Request body:
```json
{
  "question": "How do I reset my password?",
  "context": {
    "product_id": 1
  }
}
```

Response:
```json
{
  "results": [
    {
      "question": "How do I reset my password?",
      "answer": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
      "score": 0.95
    },
    // More results...
  ]
}
```

#### Get User Memory

```
GET /api/ai/memory/{user_id}
```

Response:
```json
{
  "memory": [
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
    // More memories...
  ]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found

```json
{
  "detail": "Item not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```
