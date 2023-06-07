from pydantic import BaseModel, UUID4


class UserProfileCreate(BaseModel):
    name: str
    description: str
    time: str


class UserProfileResponse(BaseModel):
    id: UUID4
    name: str
    description: str
    time: str
    user_id: int

    class Config:
        orm_mode = True
