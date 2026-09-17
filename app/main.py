# FastAPI import panrom
from fastapi import FastAPI

# Database engine and Base import panrom
from app.database import engine, Base

# models import panrom
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.models.member import Member
from app.models.borrow import BorrowRecord
from app.models.user import User

# routers import panrom
from app.routers.books import router as book_router
from app.routers.authors import router as author_router
from app.routers.categories import router as category_router
from app.routers.members import router as member_router
from app.routers.borrow import router as borrow_router
from app.routers.auth import router as auth_router


# FastAPI application create panrom
app = FastAPI(
    title="Library Book Management API"
)


# Database-la tables create pannum
Base.metadata.create_all(bind=engine)


# routers a applicationkku include panrom
app.include_router(book_router)
app.include_router(author_router)
app.include_router(category_router)
app.include_router(member_router)
app.include_router(borrow_router)
app.include_router(auth_router)