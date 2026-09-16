from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    # Member unique ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Member name
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Member email (unique-aa irukanum)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    
    # Member phone number
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)