from sqlalchemy import Boolean, Integer, Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    profile = relationship("UserProfile", uselist=False, back_populates="user")

    @classmethod
    async def find(cls, db_session: AsyncSession, email: str):
        """
        :param db_session:
        :param email:
        :return:
        """
        stmt = select(cls).where(cls.email == email)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        # if instance is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail={"Not found": f"There is no record for name: {email}"},
        #     )
        # else:
        return instance
