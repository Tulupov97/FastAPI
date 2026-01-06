from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db
from sqlalchemy.orm import Session
from app.models.categories import Category as CategoryModel
from app.models.products import Product as ProductModel
from sqlalchemy import select, update

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(dp: Session = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    products  = select(ProductModel).where(ProductModel.is_active == True)
    return dp.scalars(products).all()


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый товар.
    """
    # Проверяем, существует ли активная категория
    category = db.scalars(
        select(CategoryModel).where(CategoryModel.id == product.category_id,
                                    CategoryModel.is_active == True)
    ).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found or inactive")
        
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
    

@router.get("/category/{category_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_products_by_category(res,category_id: int):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    return {"message": f"Детали товара {category_id} (заглушка)"}


@router.get("/{product_id}")
async def get_product(product_id: int):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    return {"message": f"Детали товара {product_id} (заглушка)"}


@router.put("/{product_id}")
async def update_product(product_id: int):
    """
    Обновляет товар по его ID.
    """
    return {"message": f"Товар {product_id} обновлён (заглушка)"}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """
    Удаляет товар по его ID.
    """
    return {"message": f"Товар {product_id} удалён (заглушка)"}