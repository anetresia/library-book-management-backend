# SQLAlchemy la irunthu database column types import panrom
from sqlalchemy import Boolean, Float, String

# Mapped -> column oda Python data type specify panna
# mapped_column -> database column create panna
from sqlalchemy.orm import Mapped, mapped_column

# database.py la create panna Base-a import panrom
from app.database import Base


# Book table-ku SQLAlchemy model create panrom
class Book(Base):

    # Database-la table name "books" nu specify panrom
    __tablename__ = "books"

    # Book-ku unique ID
    # int -> ID number ah irukkum
    # primary_key=True -> ovvoru book-kum unique ID
    # index=True -> ID search fast-ah nadakka help pannum
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # Book title
    # Mapped[str] -> title text/string ah irukkum
    # String(200) -> maximum 200 characters
    # nullable=False -> title empty-ah irukka koodathu
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    # Book author name
    # Mapped[str] -> author name text/string ah irukkum
    # String(100) -> maximum 100 characters
    # nullable=False -> author name kandippa irukkanum
    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Book price
    # Mapped[float] -> price decimal value ah irukkalam
    # Float -> database-la decimal number store panna
    # nullable=False -> price kandippa irukkanum
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    # Book category
    # Mapped[str] -> category text/string ah irukkum
    # String(100) -> maximum 100 characters
    # nullable=False -> category kandippa irukkanum
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Book available-aa illayaa nu store panna
    # Mapped[bool] -> True / False value
    # Boolean -> True or False store pannum
    # default=True -> value kudukkalana automatically True
    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )