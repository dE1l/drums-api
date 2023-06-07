import uuid

from sqlalchemy import Integer, Column, String, select, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.models import Base, User
from app.schemas.user_profile import UserProfileResponse


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    time = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="profile")

    @classmethod
    async def find_by_email(cls, db_session: AsyncSession, email: str) -> UserProfileResponse:
        stmt = select(UserProfile).join(UserProfile.user).where(User.email == email)
        result = await db_session.execute(stmt)
        profile = result.scalar_one_or_none()
        return profile
