# pydantic module use panni book data validate panna model create panrom
from pydantic import BaseModel, Field


# CREATE BOOK MODEL
class BookCreate(BaseModel):

    # title minimum 2 characters irukkanum
    title: str = Field(min_length=2)

    # author minimum 2 characters irukkanum
    author: str = Field(min_length=2)

    # price 0 vida greater-aa irukkanum
    price: float = Field(gt=0)

    # book category
    category: str

    # book available-aa irukka illaya
    available: bool


# UPDATE BOOK MODEL
class BookUpdate(BaseModel):

    # update pannumbothu fields ellam optional
    title: str | None = Field(default=None, min_length=2)
    author: str | None = Field(default=None, min_length=2)
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    available: bool | None = None


# RESPONSE MODEL
class BookResponse(BaseModel):

    id: int
    title: str
    author: str
    price: float
    category: str
    available: bool