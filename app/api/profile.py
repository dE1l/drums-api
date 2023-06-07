import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.api.login import manager
from app.database import get_db
from app.models import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileResponse, UserProfileCreate

router = APIRouter(prefix="/v1/profile")


# @manager.user_loader()
@router.get("", response_model=UserProfileResponse)
async def protected_route(user=Depends(manager), db=Depends(get_db)):
    profile = await UserProfile.find_by_email(db, user["user"])
    if profile:
        return profile
    else:
        return JSONResponse(content={"message": "Profile not found"}, status_code=404)


@router.post("", response_model=UserProfileCreate)
async def create_profile(profile: UserProfileCreate, user=Depends(manager), db: AsyncSession = Depends(get_db)):
    user_data = await User.find(db, user.get("user"))
    exist_user_profile = await UserProfile.find_by_email(db, user.get("user"))

    if exist_user_profile:
        await exist_user_profile.update(db, **profile.dict())
        return JSONResponse(content={"message": "Profile updated"}, status_code=200)

    else:
        profile_data = profile.dict()
        profile_data["user_id"] = user_data.id
        db_user = UserProfile(**profile_data)

        profile = await db_user.save(db)
        return JSONResponse(content={"message": "Profile created"}, status_code=200)
