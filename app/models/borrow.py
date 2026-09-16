from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    # Unique ID for the borrow transaction
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign Keys to link Book and Member
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    
    # Borrow date (automatically today's date eduthukkum)
    borrow_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    
    # Status: "Borrowed" or "Returned"
    status: Mapped[str] = mapped_column(String(50), default="Borrowed")