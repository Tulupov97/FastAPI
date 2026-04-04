from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from app.db_depends import AsyncSession, get_async_db
from app.models import Order as OrderModel
from app.schemas import OrderList


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=OrderList)
async def get_orders(
    page: int = Query(1, ge=1, description="Номер страницы (≥ 1)"),
    page_size: int = Query(
        20, ge=1, le=100, description="Количество элементов на странице (1–100)"),
    db: AsyncSession = Depends(get_async_db)
):
    # Подсчёт общего количества активных заказов
    count_stmt = select(func.count()).select_from(
        OrderModel).where(OrderModel.is_active == True)
    total = await db.scalar(count_stmt) or 0

    # Пагинация: offset и limit
    offset = (page - 1) * page_size
    stmt = (
        select(OrderModel)
        .where(OrderModel.is_active == True)
        .offset(offset)
        .limit(page_size)
        .order_by(OrderModel.id)
    )
    result = await db.scalars(stmt)
    orders = result.all()

    return OrderList(
        items=orders,
        total=total,
        page=page,
        page_size=page_size
    )
