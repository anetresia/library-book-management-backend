from sqlalchemy import Float, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    # author_id use panni Author object connect panrom
    author = relationship("Author")

    # category_id use panni Category object connect panrom
    category = relationship("Category")