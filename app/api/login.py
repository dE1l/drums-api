import os

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager

from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/v1/auth")


manager = LoginManager(os.getenv("LOGIN_MANAGER_SECRET"), "/v1/auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user: UserCreate, db=Depends(get_db)):
    if await User.find(db, user.email) is not None:
        raise HTTPException(status_code=400, detail="A user with this email already exists")
    else:
        user_data = user.dict()
        user_data["password"] = hash_password(user.password)
        db_user = User(**user_data)
        await db_user.save(db)
        return db_user


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db)):
    email = data.username
    password = data.password

    user = await User.find(db_session, email)  # we are using the same function to retrieve the user
    if user is None:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif not verify_password(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data=dict(sub=user.email))
    return {"access_token": access_token, "token_type": "Bearer"}


@manager.user_loader()
def _get_user(user=Depends(manager)):
    return user


def hash_password(plaintext_password: str):
    """Return the hash of a password"""
    return manager.pwd_context.hash(plaintext_password)


def verify_password(password_input: str, hashed_password: str):
    """Check if the provided password matches"""
    return manager.pwd_context.verify(password_input, hashed_password)
