# Pydantic module use panni
# book data validate panna schemas create panrom

from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# CREATE BOOK MODEL
# ==========================================

class BookCreate(BaseModel):

    # Book title minimum 2 characters irukkanum
    title: str = Field(min_length=2)

    # Author name minimum 2 characters irukkanum
    author: str = Field(min_length=2)

    # Price 0 vida greater-aa irukkanum
    price: float = Field(gt=0)

    # Book category
    category: str = Field(min_length=2)

    # Book available-aa irukka illaya
    available: bool = True

    # Book stock
    stock: int = Field(default=0, ge=0)


# ==========================================
# UPDATE BOOK MODEL
# ==========================================

class BookUpdate(BaseModel):

    # Update pannumbothu fields ellam optional

    # Book title update
    title: str | None = Field(
        default=None,
        min_length=2
    )

    # Author name update
    author: str | None = Field(
        default=None,
        min_length=2
    )

    # Price update
    price: float | None = Field(
        default=None,
        gt=0
    )

    # Category update
    category: str | None = Field(
        default=None,
        min_length=2
    )

    # Available status update
    available: bool | None = None

    # Stock update
    stock: int | None = Field(
        default=None,
        ge=0
    )


# ==========================================
# RESPONSE MODEL
# ==========================================

class BookResponse(BaseModel):

    # Database book ID
    id: int

    # Book title
    title: str

    # Author name
    author: str

    # Book price
    price: float

    # Category name
    category: str

    # Available status
    available: bool

    # Book stock
    stock: int

    # SQLAlchemy model-la irukkura
    # relationship data-va Pydantic read panna allow panrom
    model_config = ConfigDict(
        from_attributes=True
    )