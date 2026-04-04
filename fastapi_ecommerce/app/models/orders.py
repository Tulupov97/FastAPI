from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    total_price: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
