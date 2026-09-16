from pydantic import BaseModel, Field

# CREATE CATEGORY MODEL
class CategoryCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str | None = None

# UPDATE CATEGORY MODEL
class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    description: str | None = None

# RESPONSE MODEL
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True