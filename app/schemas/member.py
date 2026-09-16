from pydantic import BaseModel, EmailStr, Field

# CREATE MEMBER MODEL
class MemberCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: str | None = None

# UPDATE MEMBER MODEL
class MemberUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    phone: str | None = None

# RESPONSE MODEL
class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None

    class Config:
        from_attributes = True