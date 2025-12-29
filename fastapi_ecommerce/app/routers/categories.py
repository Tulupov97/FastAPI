from fastapi import APIRouter

router = APIRouter(prefix='/categories', tags=['categories'])

@router.get("/")
async def get_all_categories():
    """Возвращает список вех категорий"""
    return {"message" : "Список всех категорий pass"}

@router.post("/")
async def create_category():
    """Создаем новую категорию"""
    return {"message": "Категория создана pass"}

@router.put("/{category_id}")
async def update_category(category_id: int):
    """
    Обновляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} обновлена (заглушка)"}


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    """
    Удаляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} удалена (заглушка)"}