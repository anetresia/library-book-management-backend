from pydantic import BaseModel
from datetime import date

# BORROW CREATE MODEL (Book ID and Member ID kudutha pothum)
class BorrowCreate(BaseModel):
    book_id: int
    member_id: int

# RESPONSE MODEL
class BorrowResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrow_date: date
    status: str

    class Config:
        from_attributes = True