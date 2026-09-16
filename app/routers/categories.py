from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

# Category router create panrom
router = APIRouter(prefix="/categories", tags=["Categories"])


# =========================================================
# 1. GET ALL CATEGORIES
# =========================================================
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# =========================================================
# 2. GET CATEGORY BY ID
# =========================================================
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    return category


# =========================================================
# 3. CREATE CATEGORY
# =========================================================
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Category name already irukkaa nu check panrom
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Category already exists"
        )
    
    new_category = Category(
        name=category.name, 
        description=category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# =========================================================
# 4. UPDATE CATEGORY
# =========================================================
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category_update: CategoryUpdate, 
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    
    update_data = category_update.model_dump(exclude_unset=True)
    
    if "name" in update_data:
        category.name = update_data["name"]
    if "description" in update_data:
        category.description = update_data["description"]
        
    db.commit()
    db.refresh(category)
    return category


# =========================================================
# 5. DELETE CATEGORY
# =========================================================
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}