from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.utils.database.db_depends import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from sqlalchemy import select
from app.auth import get_current_buyer
from app.rating import update_product_rating

from logging import getLogger

logger = getLogger(__name__)


router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """Все отзывы"""
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return reviews.all()


@router.get("/{product_id}", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_reviews_by_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """Отзывы по продукту"""
    if not await db.scalar(select(ProductModel).where(ProductModel.id == product_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.product_id == product_id, ReviewModel.is_active == True))
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_buyer)):
    if not await db.scalar(select(ProductModel).where(ProductModel.id == review.product_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await update_product_rating(review.product_id, db)
    await db.refresh(db_review)  # Для получения id и is_active из базы
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_buyer)):
    review = await db.scalar(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True))
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    review.is_active = False
    await update_product_rating(review.product_id, db)
    await db.commit()
    await db.refresh(review)  # Для возврата is_active = False
    return {"message": "Review deleted"}
