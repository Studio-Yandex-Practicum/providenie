from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import UserTG


async def check_tg_id_unique(
        pydantic_scheme_user: str,
        session: AsyncSession,
) -> None:
    """Check unique telegram id for new user."""
    tg_id = pydantic_scheme_user.tg_id
    existing_user_query = select(UserTG).where(UserTG.tg_id == tg_id)
    result = await session.execute(existing_user_query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this tg_id already exists.")
