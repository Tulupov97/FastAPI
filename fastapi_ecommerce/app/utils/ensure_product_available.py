from fastapi import HTTPException, status
from sqlalchemy import select
from app.models.products import Product as ProductModel
from sqlalchemy.ext.asyncio import AsyncSession


async def _ensure_product_available(db: AsyncSession, product_id: int) -> None:
    result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.is_active == True,
        )
    )
    product = result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
