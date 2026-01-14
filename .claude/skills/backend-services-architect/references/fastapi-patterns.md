# FastAPI CRUD Patterns

## Request/Response Model Template

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Create user request"""
    email: str = Field(..., min_length=5, max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    @validator('email')
    def email_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    """User response model"""
    id: str
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True  # For ORM models

class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
```

## CRUD Endpoint Template

```python
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post('/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        # Check for duplicate
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this email already exists'
            )

        db_user = User(email=user.email, username=user.username)
        db_user.set_password(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f'User created: {db_user.id}')
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f'Error creating user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create user'
        )

# READ (Single)
@app.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user

# READ (List with pagination)
@app.get('/users', response_model=list[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """List all users with pagination"""
    users = db.query(User).offset(pagination.offset).limit(pagination.limit).all()
    return users

# UPDATE
@app.put('/users/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserCreate,
    db: Session = Depends(get_db)
):
    """Update user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    try:
        user.email = user_update.email
        user.username = user_update.username
        db.commit()
        db.refresh(user)
        logger.info(f'User updated: {user_id}')
        return user
    except Exception as e:
        db.rollback()
        logger.error(f'Error updating user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update user'
        )

# DELETE
@app.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    try:
        db.delete(user)
        db.commit()
        logger.info(f'User deleted: {user_id}')
    except Exception as e:
        db.rollback()
        logger.error(f'Error deleting user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete user'
        )
```

## Error Response Schema

```python
from typing import Optional

class ErrorDetail(BaseModel):
    code: str  # e.g., "VALIDATION_ERROR", "NOT_FOUND"
    message: str
    details: Optional[dict] = None

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': str(exc)
            }
        }
    )
```

## Idempotency Pattern

```python
from uuid import uuid4

@app.post('/payments', response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    idempotency_key: str = Header(...),
    db: Session = Depends(get_db)
):
    """Create payment with idempotency key"""
    # Check if already processed
    existing = db.query(Payment).filter(
        Payment.idempotency_key == idempotency_key
    ).first()

    if existing:
        return existing

    # Process new payment
    db_payment = Payment(
        amount=payment.amount,
        idempotency_key=idempotency_key
    )
    db.add(db_payment)
    db.commit()
    return db_payment
```

## Request Logging with Correlation ID

```python
from uuid import uuid4
from fastapi import Request
import time

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get('x-correlation-id', str(uuid4()))
    request.state.correlation_id = correlation_id

    start_time = time.time()
    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        f'Request completed',
        extra={
            'correlation_id': correlation_id,
            'method': request.method,
            'path': request.url.path,
            'status': response.status_code,
            'duration_ms': duration * 1000
        }
    )

    response.headers['x-correlation-id'] = correlation_id
    return response
```
