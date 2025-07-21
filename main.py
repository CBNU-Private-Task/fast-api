from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.database import Base, engine
from app.model import user, article
from app.core.exceptions import http_exception_handler, validation_exception_handler

user.Base.metadata.create_all(bind=engine)
article.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="My Streaming App",
    description="This is a streaming application built with FastAPI and SQLAlchemy.",
    version="1.0.0",
)

# CORS Middleware
origins = [
    "*",  # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router, prefix="/api/v1")
