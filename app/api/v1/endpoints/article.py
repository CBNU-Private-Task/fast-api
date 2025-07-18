from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import identity

from app.schemas.article import ArticleResponse, ArticleCreate, ArticleUpdate
from app.schemas.response import ApiResponse
from app.db.database import get_db
from app.model.article import Article
from app.core.Oauth import get_current_user
from app.model.user import User

router = APIRouter()


# Get all article
@router.get(
    "/articles",
    response_model=ApiResponse[List[ArticleResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get all articles",
)
def get_articles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    articles = db.query(Article).filter(Article.owner_id == current_user.id).all()
    return {"data": articles}


# Get Article By ID
@router.get(
    "/article/{id}",
    response_model=ApiResponse[ArticleResponse],
    status_code=status.HTTP_200_OK,
    summary="Get article by ID",
)
def get_article_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    article_id = db.query(Article).filter(Article.id == id, Article.owner_id == current_user.id).first()

    if article_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The id: {id} you requested for does not exist",
        )
    return {"data": article_id}

# Create new Article
@router.post(
    "/articles",
    response_model=ApiResponse[ArticleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
)
def create_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_article = Article(**article.model_dump(), owner_id=current_user.id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return {"data": new_article, "message": "Article created successfully"}

# Delete new Article
@router.delete(
     "/article/{id}",
     status_code=status.HTTP_200_OK,
     summary="Delete Article",
     response_model=ApiResponse[None]
)
def delete_article(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_article = db.query(Article).filter(Article.id == id, Article.owner_id == current_user.id)
    
    if deleted_article.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_article.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"Article with id {id} has been deleted!"}

# Update Article
@router.put(
     "/article/{id}",
     response_model=ApiResponse[ArticleResponse],
     status_code=status.HTTP_200_OK,
     summary="Update Article"
)
def update_article(id: int, article_update: ArticleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == id, Article.owner_id == current_user.id).first()

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    
    update_data = article_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return {"data": article, "message": f"Article with id {id} updated successfully"}