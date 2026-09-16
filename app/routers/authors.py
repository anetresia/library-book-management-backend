from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse

# author router create panrom
router = APIRouter(prefix="/authors", tags=["Authors"])


# =========================================================
# GET ALL AUTHORS
# =========================================================
@router.get("/", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


# =========================================================
# GET ONE AUTHOR
# =========================================================
@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


# =========================================================
# CREATE AUTHOR
# =========================================================
@router.post(
    "/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED
)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_author = db.query(Author).filter(Author.email == author.email).first()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_author = Author(
        name=author.name, email=author.email, country=author.country
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


# =========================================================
# UPDATE AUTHOR
# =========================================================
@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)
):
    author = db.query(Author).filter(Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    update_data = author_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        author.name = update_data["name"]
    if "email" in update_data:
        author.email = update_data["email"]
    if "country" in update_data:
        author.country = update_data["country"]

    db.commit()
    db.refresh(author)
    return author


# =========================================================
# DELETE AUTHOR
# =========================================================
@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}