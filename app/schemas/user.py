from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True
