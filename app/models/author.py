from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Author(Base):

    __tablename__ = "authors"

    # Author unique ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Author name (minimum 2 characters validation schema-la varum)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Author email (unique-aa irukanum)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, index=True, nullable=False
    )

    # Author country
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationship: One Author has Many Books (Optional, but useful)
    # books = relationship("Book", back_populates="author")