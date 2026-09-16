from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.borrow import BorrowRecord
from app.models.book import Book
from app.models.member import Member
from app.schemas.borrow import BorrowCreate, BorrowResponse

router = APIRouter(prefix="/borrow", tags=["Borrow & Return"])

# 1. Get All Borrow Records
@router.get("/", response_model=list[BorrowResponse])
def get_borrow_records(db: Session = Depends(get_db)):
    return db.query(BorrowRecord).all()

# 2. Borrow a Book (POST)
@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(record: BorrowCreate, db: Session = Depends(get_db)):
    # Book irukkaa nu check panrom
    book = db.query(Book).filter(Book.id == record.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # Member irukkaa nu check panrom
    member = db.query(Member).filter(Member.id == record.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
        
    # New borrow record create panrom
    new_record = BorrowRecord(
        book_id=record.book_id,
        member_id=record.member_id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# 3. Return a Book (PUT / Update status to Returned)
@router.put("/{record_id}/return", response_model=BorrowResponse)
def return_book(record_id: int, db: Session = Depends(get_db)):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
        
    if record.status == "Returned":
        raise HTTPException(status_code=400, detail="Book is already returned")
        
    record.status = "Returned"
    db.commit()
    db.refresh(record)
    return record