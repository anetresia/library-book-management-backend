# FastAPI packages import panrom
from fastapi import APIRouter, HTTPException, status, Depends

# SQLAlchemy Session import panrom
from sqlalchemy.orm import Session

# Database-la irunthu DB session edukka get_db import panrom
from app.database import get_db

# SQLAlchemy models import panrom
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category

# Pydantic schemas import panrom
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse
)

# User authentication and authorization functions import panrom
from app.auth.security import (
    get_current_user,
    require_admin,
    require_librarian
)


# =========================================================
# BOOK ROUTER
# =========================================================

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# =========================================================
# GET ALL BOOKS
# =========================================================

@router.get("/", response_model=list[BookResponse])
def get_books(
    category: str | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Database-la Book table-ai query panrom
    query = db.query(Book)

    # max_price filter
    if max_price is not None:

        # max_price vida kuraiya/samamaana books
        query = query.filter(Book.price <= max_price)

    # Books database-la irunthu edukrom
    books = query.all()

    # Response list create panrom
    result = []

    for book in books:

        # Category filter
        if category is not None:
            if book.category.name != category:
                continue

        # Book data-va response format-ku convert panrom
        result.append(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "price": book.price,
                "category": book.category.name,
                "available": book.available,
                "stock": book.stock
            }
        )

    return result


# =========================================================
# GET ONE BOOK
# =========================================================

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # book_id use panni book search panrom
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    # Book kidaikkalana 404
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Book response create panrom
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "price": book.price,
        "category": book.category.name,
        "available": book.available,
        "stock": book.stock
    }


# =========================================================
# CREATE BOOK
# =========================================================

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_librarian)
):

    # Author name use panni author search panrom
    author = db.query(Author).filter(
        Author.name == book.author
    ).first()

    # Author kidaikkalana new author create panrom
    if author is None:

        author = Author(
            name=book.author,
            email=f"{book.author.lower().replace(' ', '.')}@example.com",
            country=None
        )

        db.add(author)
        db.flush()

    # Category name use panni category search panrom
    category = db.query(Category).filter(
        Category.name == book.category
    ).first()

    # Category kidaikkalana new category create panrom
    if category is None:

        category = Category(
            name=book.category,
            description=None
        )

        db.add(category)
        db.flush()

    # New Book create panrom
    new_book = Book(
        title=book.title,
        price=book.price,
        stock=book.stock,
        available=book.available,
        author_id=author.id,
        category_id=category.id
    )

    # Database-la add panrom
    db.add(new_book)

    # Changes save panrom
    db.commit()

    # New book data refresh panrom
    db.refresh(new_book)

    # Response return panrom
    return {
        "id": new_book.id,
        "title": new_book.title,
        "author": author.name,
        "price": new_book.price,
        "category": category.name,
        "available": new_book.available,
        "stock": new_book.stock
    }


# =========================================================
# UPDATE BOOK
# =========================================================

@router.put(
    "/{book_id}",
    response_model=BookResponse
)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_librarian)
):

    # Book search panrom
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    # Book kidaikkalana 404
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # User send panna fields mattum edukrom
    update_data = book_update.model_dump(
        exclude_unset=True
    )

    # -----------------------------------------
    # TITLE
    # -----------------------------------------

    if "title" in update_data:
        book.title = update_data["title"]

    # -----------------------------------------
    # PRICE
    # -----------------------------------------

    if "price" in update_data:
        book.price = update_data["price"]

    # -----------------------------------------
    # AVAILABLE
    # -----------------------------------------

    if "available" in update_data:
        book.available = update_data["available"]

    # -----------------------------------------
    # STOCK
    # -----------------------------------------

    if "stock" in update_data:
        book.stock = update_data["stock"]

    # -----------------------------------------
    # AUTHOR
    # -----------------------------------------

    if "author" in update_data:

        author = db.query(Author).filter(
            Author.name == update_data["author"]
        ).first()

        # Author illana new author create panrom
        if author is None:

            author = Author(
                name=update_data["author"],
                email=f"{update_data['author'].lower().replace(' ', '.')}@example.com",
                country=None
            )

            db.add(author)
            db.flush()

        # Book-oda author_id update panrom
        book.author_id = author.id

    # -----------------------------------------
    # CATEGORY
    # -----------------------------------------

    if "category" in update_data:

        category = db.query(Category).filter(
            Category.name == update_data["category"]
        ).first()

        # Category illana new category create panrom
        if category is None:

            category = Category(
                name=update_data["category"],
                description=None
            )

            db.add(category)
            db.flush()

        # Book-oda category_id update panrom
        book.category_id = category.id

    # Changes save panrom
    db.commit()

    # Updated book refresh panrom
    db.refresh(book)

    # Updated response return panrom
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "price": book.price,
        "category": book.category.name,
        "available": book.available,
        "stock": book.stock
    }


# =========================================================
# DELETE BOOK
# =========================================================

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    # Book search panrom
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    # Book kidaikkalana 404
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Book delete panrom
    db.delete(book)

    # Changes save panrom
    db.commit()

    # Success response
    return {
        "message": "Book deleted successfully"
    }