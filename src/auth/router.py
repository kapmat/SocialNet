from fastapi import APIRouter

from auth.base_config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate, UserUpdate

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