from pydantic import BaseModel, Field
from typing import Optional, Any, cast
from datetime import datetime, timezone
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: ErrorDetail
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

async def http_exception_handler(request: Request, exc: Exception):
    """
    Handles HTTPErrors and formats them into the standard error response.
    """
    http_exc = cast(HTTPException, exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=ErrorResponse(
            message=http_exc.detail,
            error=ErrorDetail(code=f"HTTP_{http_exc.status_code}", message=http_exc.detail)
        ).model_dump(mode="json")
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """
    Handles Pydantic validation errors and formats them.
    """
    validation_exc = cast(RequestValidationError, exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message="Input validation failed",
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="One or more fields failed validation.",
                details=validation_exc.errors()
            )
        ).model_dump(mode="json")
    ) 