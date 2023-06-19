from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import fastapi_users, auth_backend, current_user
from auth.schemas import UserRead, UserCreate, UserUpdate, UsersList
from auth.models import User
from database import get_async_session


router = APIRouter(
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt"
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)


@router.get("/users", response_model=list[UsersList])
async def get_all_users(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    users = await session.execute(select(User))
    return [UsersList(id=user.id, first_name=user.first_name, last_name=user.last_name) for user in users.scalars()]
