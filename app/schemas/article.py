from pydantic import BaseModel
from datetime import datetime
from typing import List

class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool = True

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

