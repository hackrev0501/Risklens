from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "developer"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
