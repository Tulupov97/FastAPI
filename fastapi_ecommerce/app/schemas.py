from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Annotated
from fastapi import Form

class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """
    name: str = Field(..., min_length=3, max_length=50,
                      description="Название категории (3-50 символов)")
    parent_id: int | None = Field(
        None, description="ID родительской категории, если есть")


class Category(CategoryCreate):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор категории")
    is_active: bool = Field(..., description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """
    name: str = Field(..., min_length=3, max_length=100,
                      description="Название товара (3-100 символов)")
    description: str | None = Field(None, max_length=500,
                                    description="Описание товара (до 500 символов)")
    price: Decimal = Field(..., gt=0,
                           description="Цена товара (больше 0)", decimal_places=2)
    stock: int = Field(..., ge=0,
                       description="Количество товара на складе (0 или больше)")
    category_id: int = Field(...,
                             description="ID категории, к которой относится товар")
    
    @classmethod
    def as_form(
            cls,
            name: Annotated[str, Form(...)],
            price: Annotated[Decimal, Form(...)],
            stock: Annotated[int, Form(...)],
            category_id: Annotated[int, Form(...)],
            description: Annotated[str | None, Form()] = None,
    ) -> "ProductCreate":
        return cls(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
        )   


class Product(ProductCreate):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор товара")
    rating: float = Field(..., ge=0, le=5,
                          description="Средняя оценка товара (0-5)")
    image_url: str | None = Field(None, description="URL изображения товара")
    is_active: bool = Field(..., description="Активность товара")

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """
    Список пагинации для товаров.
    """
    items: list[Product] = Field(description="Товары для текущей страницы")
    total: int = Field(ge=0, description="Общее количество товаров")
    page: int = Field(ge=1, description="Номер текущей страницы")
    page_size: int = Field(
        ge=1, description="Количество элементов на странице")

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(
        min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer", pattern="^(buyer|seller)$",
                      description="Роль: 'buyer' или 'seller'")


class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    product_id: int = Field(...,
                            description="ID товара, к которому относится отзыв")
    comment: str | None = Field(
        None, max_length=500, description="Комментарий (до 500 символов)")
    grade: int = Field(..., ge=1, le=5, description="Оценка товара (1-5)")
    model_config = ConfigDict(from_attributes=True)


class Review(ReviewCreate):
    id: int
    user_id: int = Field(..., description="ID пользователя, оставившего отзыв")
    is_active: bool = Field(..., description="Активность отзыва")
    comment_date: datetime = Field(...,
                                   description="Дата и время создания отзыва")
    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Order(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    is_active: bool = True


class OrderList(BaseModel):
    """
    Список пагинации для заказов.
    """
    items: list[Order] = Field(description="Заказы для текущей страницы")
    total: int = Field(description="Общее количество заказов")
    page: int = Field(ge=1, description="Номер текущей страницы")
    page_size: int = Field(
        ge=1, description="Количество элементов на странице")

    model_config = ConfigDict(from_attributes=True)


class CartItemBase(BaseModel):
    product_id: int = Field(description="ID товара")
    quantity: int = Field(ge=1, description="Количество товара")

class CartItemCreate(CartItemBase):
    """Модель для добавления нового товара в корзину."""
    pass

class CartItemUpdate(BaseModel):
    """Модель для обновления количества товара в корзине."""
    quantity: int = Field(..., ge=1, description="Новое количество товара")

class CartItem(BaseModel):
    """Товар в корзине с данными продукта."""
    id: int = Field(..., description="ID позиции корзины")
    quantity: int = Field(..., ge=1, description="Количество товара")
    product: Product = Field(..., description="Информация о товаре")

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """Полная информация о корзине пользователя."""
    user_id: int = Field(..., description="ID пользователя")
    items: list[CartItem] = Field(default_factory=list, description="Содержимое корзины")
    total_quantity: int = Field(..., ge=0, description="Общее количество товаров")
    total_price: Decimal = Field(..., ge=0, description="Общая стоимость товаров")

    model_config = ConfigDict(from_attributes=True)


