from fastapi import APIRouter, Depends, Query, HTTPException
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
        db: AsyncSession = Depends(get_async_db),
        status: str | None = Query(
            pattern="^(paid|cancel)$", discription="Статус заказа", default=None),
        min_price: float = Query(
            ge=1, default=1, discription="Минимальная цена"),
        max_price: float = Query(ge=1, default=999999, discription="Максимальная цена")):
    """Получение всех заказов по фильтру"""

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price не может быть больше max_price")
    
    filters = [OrderModel.is_active == True]
    if status is not None:
        filters.append(OrderModel.status == status)
    if min_price is not None:
        filters.append(OrderModel.total_price >= min_price)
    if max_price is not None:
        filters.append(OrderModel.total_price <= max_price)
    

    # Подсчёт общего количества активных заказов c учётом фильтров
    count_stmt = select(func.count()).select_from(
        OrderModel).where(*filters)
    total = await db.scalar(count_stmt) or 0

    # Пагинация: offset и limit
    offset = (page - 1) * page_size
    stmt = (
        select(OrderModel)
        .where(*filters)
        .offset(offset)
        .limit(page_size)
        .order_by(OrderModel.id)
    )
    orders = (await db.scalars(stmt)).all()

    return OrderList(
        items=orders,
        total=total,
        page=page,
        page_size=page_size
    )
