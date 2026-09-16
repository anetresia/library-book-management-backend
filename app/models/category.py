from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    # Category unique ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Category name (e.g., Programming, Fiction, Science)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    # Category description (optional)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)