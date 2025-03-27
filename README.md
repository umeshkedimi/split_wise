# SplitWise API

A FastAPI-based backend application for managing group expenses and settlements.

## Features

- User management
- Group creation and management
- Expense tracking
- Balance calculation
- Docker support

## Prerequisites

- Python 3.11+
- Docker and Docker Compose

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd split_wise
```

2. Build and run using Docker:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user details

### Groups
- `POST /groups/` - Create a new group
- `GET /groups/{group_id}` - Get group details

### Expenses
- `POST /expenses/` - Create a new expense
- `GET /expenses/group/{group_id}` - Get all expenses in a group
- `GET /expenses/user/{user_id}` - Get all expenses for a user
- `GET /balance/{user_id}/{group_id}` - Get user's balance in a group

## Example Usage

1. Create a user:
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}'
```

2. Create a group:
```bash
curl -X POST "http://localhost:8000/groups/" -H "Content-Type: application/json" -d '{
    "name": "Vacation Group",
    "description": "Group for vacation expenses"
}'
```

3. Add an expense:
```bash
curl -X POST "http://localhost:8000/expenses/" -H "Content-Type: application/json" -d '{
    "description": "Dinner",
    "amount": 100.00,
    "group_id": "group-uuid",
    "splits": [
        {"user_id": "user1-uuid", "amount": 50.00},
        {"user_id": "user2-uuid", "amount": 50.00}
    ]
}'
```

## Development

The project follows a repository pattern with the following structure:
- `app/api/v1/` - API routes
- `app/core/` - Core configurations
- `app/models/` - Database models
- `app/repositories/` - Repository layer
- `app/schemas/` - Pydantic schemas
- `app/services/` - Business logic 