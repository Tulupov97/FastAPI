from sqlalchemy.sql import func
from sqlalchemy import select
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.db_depends import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def update_product_rating(product_id: int, db: AsyncSession):
    """Обновление рейтинга продукта"""
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()