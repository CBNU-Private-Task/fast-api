from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional
from datetime import datetime, timezone

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """
    A generic and standardized API response model.
    """
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Optional[T] = None

class ListResponse(BaseModel, Generic[T]):
    """
    A generic response model for returning a list of items.
    """
    status: str = "success"
    count: int
    results: List[T]

class DetailResponse(BaseModel, Generic[T]):
    """
    A generic response model for returning a single item detail.
    """
    status: str = "success"
    result: T 