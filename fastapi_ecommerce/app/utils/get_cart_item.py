from sqlalchemy import select
from app.models.cart_items import CartItem as CartItemModel
from app.db_depends import AsyncSession
from sqlalchemy.orm import selectinload

async def _get_cart_item(
    db: AsyncSession, user_id: int, product_id: int
) -> CartItemModel | None:
    result = await db.scalars(
        select(CartItemModel)
        .options(selectinload(CartItemModel.product))
        .where(
            CartItemModel.user_id == user_id,
            CartItemModel.product_id == product_id,
        )
    )
    return result.first()