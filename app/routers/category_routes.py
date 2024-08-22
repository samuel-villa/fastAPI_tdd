import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal, get_db_session
from app.models import Category
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryDeleteReturn,
    CategoryReturn,
    CategoryUpdate,
)
from app.utils.category_utils import check_existing_category

router = APIRouter()
db = SessionLocal()

# logger = logging.getLogger(__name__)  # __name__=app.routers.category_routes
logger = logging.getLogger("app")


# Delete existing category
@router.delete("/{category_id}", response_model=CategoryDeleteReturn)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db_session),
):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db.delete(category)
        db.commit()
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Update existing category
@router.put("/{category_id}", response_model=CategoryReturn, status_code=201)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db_session),
):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        for key, value in category_data.model_dump().items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get a single category by slug
@router.get("/slug/{category_slug}", response_model=CategoryReturn)
def get_category_by_slug(category_slug: str, db: Session = Depends(get_db_session)):
    try:
        category = db.query(Category).filter(Category.slug == category_slug).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category does not exist")
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while retrieving category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get all categories
@router.post("/", response_model=CategoryReturn, status_code=201)
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db_session)
):
    try:
        check_existing_category(db, category_data)
        new_category = Category(**category_data.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)  # refresh object state
        return new_category

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=List[CategoryReturn])
def get_categories(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        logger.error(f"Unexpected error while retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
