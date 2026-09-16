# FastAPI package-la APIRouter, HTTPException, status, Depends import panrom
from fastapi import APIRouter, HTTPException, status, Depends

# SQLAlchemy Session import panrom
from sqlalchemy.orm import Session

# Database-la irunthu DB session edukka get_db import panrom
from app.database import get_db

# SQLAlchemy Book model import panrom
from app.models.book import Book

# Pydantic schemas import panrom
from app.schemas.book import BookCreate, BookUpdate, BookResponse


# book router create panrom
router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# =========================================================
# GET ALL BOOKS
# =========================================================

# all books-a get panna GET endpoint
@router.get("/", response_model=list[BookResponse])
def get_books(
    category: str | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):

    # Database-la irukkura Book table-ai query panrom
    query = db.query(Book)

    # category filter kuduthiruntha
    if category is not None:

        # category match aagura books mattum filter panrom
        query = query.filter(Book.category == category)

    # max_price filter kuduthiruntha
    if max_price is not None:

        # max_price vida kuraiya allathu samama irukkura books filter panrom
        query = query.filter(Book.price <= max_price)

    # database-la irunthu result eduthu return panrom
    return query.all()


# =========================================================
# GET ONE BOOK
# =========================================================

# particular book-a ID use panni edukka GET endpoint
@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    # book_id match aagura book database-la search panrom
    book = db.query(Book).filter(Book.id == book_id).first()

    # book kidaikkalana 404 error
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # book kidaichaa return panrom
    return book


# =========================================================
# CREATE BOOK
# =========================================================

# new book create panna POST endpoint
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):

    # Pydantic data-va SQLAlchemy Book object-aa convert panrom
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        category=book.category,
        available=book.available
    )

    # new book-a database session-kulla add panrom
    db.add(new_book)

    # database-la changes save panrom
    db.commit()

    # database generate panna new ID and other values refresh panrom
    db.refresh(new_book)

    # newly created book return panrom
    return new_book


# =========================================================
# UPDATE BOOK
# =========================================================

# existing book-a update panna PUT endpoint
@router.put(
    "/{book_id}",
    response_model=BookResponse
)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):

    # book_id use panni database-la book search panrom
    book = db.query(Book).filter(Book.id == book_id).first()

    # book kidaikkalana 404 error
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # user kudutha fields mattum edukkrom
    update_data = book_update.model_dump(
        exclude_unset=True
    )

    # title iruntha update panrom
    if "title" in update_data:
        book.title = update_data["title"]

    # author iruntha update panrom
    if "author" in update_data:
        book.author = update_data["author"]

    # price iruntha update panrom
    if "price" in update_data:
        book.price = update_data["price"]

    # category iruntha update panrom
    if "category" in update_data:
        book.category = update_data["category"]

    # available iruntha update panrom
    if "available" in update_data:
        book.available = update_data["available"]

    # updated data database-la save panrom
    db.commit()

    # updated book data refresh panrom
    db.refresh(book)

    # updated book return panrom
    return book


# =========================================================
# DELETE BOOK
# =========================================================

# book delete panna DELETE endpoint
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    # book_id use panni database-la book search panrom
    book = db.query(Book).filter(Book.id == book_id).first()

    # book kidaikkalana 404 error
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # book-a database-la irunthu delete panrom
    db.delete(book)

    # delete change save panrom
    db.commit()

    # success message return panrom
    return {
        "message": "Book deleted successfully"
    }