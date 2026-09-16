from pydantic import BaseModel, EmailStr, Field


# CREATE AUTHOR MODEL
class AuthorCreate(BaseModel):

    # name minimum 2 characters irukkanum
    name: str = Field(min_length=2)

    # email valid email format-la irukanum
    email: EmailStr

    # country optional
    country: str | None = None


# UPDATE AUTHOR MODEL
class AuthorUpdate(BaseModel):

    # update pannumbothu ellame optional
    name: str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    country: str | None = None


# RESPONSE MODEL
class AuthorResponse(BaseModel):

    id: int
    name: str
    email: str
    country: str | None = None