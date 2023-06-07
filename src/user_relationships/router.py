import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from user_relationships.models import Relationship as Rs
from database import get_async_session


router = APIRouter(
    prefix="/user_relationships",
    tags=["Friends"]
)


@router.get("")
async def get_friend_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Rs.another_user_id).where(Rs.user_id == user.id, Rs.status_id == 3)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/requests/out")
async def get_friend_out_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Rs.another_user_id).where(Rs.user_id == user.id,  Rs.status_id == 2)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/requests/in")
async def get_friend_in_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Rs.another_user_id).where(Rs.user_id == user.id,  Rs.status_id == 1)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("")
async def add_friend_request(
        new_friend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if new_friend_id == user.id:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        result = await session.execute(select(Rs).where(Rs.user_id == user.id, Rs.another_user_id == new_friend_id))

        if len(result.all()):
            raise HTTPException(status_code=400, detail="Заявка уже отправлена")

        stmt = insert(Rs).values(user_id=user.id, another_user_id=new_friend_id, status_id=2)
        await session.execute(stmt)
        stmt = insert(Rs).values(user_id=new_friend_id, another_user_id=user.id, status_id=1)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Пользователю {new_friend_id} отправлена заявка",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception:
        return {
            "status_code": 400,
            "detail": f"Недопустимое значение",
            "headers": None
        }


@router.patch("")
async def add_friend(
        new_friend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = update(Rs)\
            .values(status_id=3)\
            .where(Rs.user_id == user.id, Rs.another_user_id == new_friend_id, Rs.status_id == 1)
        result = await session.execute(stmt)

        if not result.rowcount:
            raise Exception

        stmt = update(Rs)\
            .values(status_id=3)\
            .where(Rs.user_id == new_friend_id, Rs.another_user_id == user.id, Rs.status_id == 2)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Пользователь {new_friend_id} добавлен в друзья",
            "headers": None
        }
    except Exception:
        return HTTPException(status_code=400, detail="Недопустимое значение")