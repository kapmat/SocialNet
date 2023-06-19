from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, join
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from user_relationships.models import Relationship as Rs
from database import get_async_session
from user_relationships.schemas import UsersList

router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)


@router.get("", response_model=list[UsersList])
async def get_friend_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(User).join(Rs, User.id == Rs.user_2_id).where(Rs.user_1_id == user.id, Rs.status_id == 3)
    result = await session.execute(query)
    return [UsersList(id=user.id, first_name=user.first_name, last_name=user.last_name) for user in result.scalars()]


@router.get("/requests/out", response_model=list[UsersList])
async def get_friend_out_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(User).join(Rs, User.id == Rs.user_2_id).where(Rs.user_1_id == user.id,  Rs.status_id == 2)
    result = await session.execute(query)
    return [UsersList(id=user.id, first_name=user.first_name, last_name=user.last_name) for user in result.scalars()]


@router.get("/requests/in", response_model=list[UsersList])
async def get_friend_in_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(User).join(Rs, User.id == Rs.user_2_id).where(Rs.user_1_id == user.id, Rs.status_id == 1)
    result = await session.execute(query)
    return [UsersList(id=user.id, first_name=user.first_name, last_name=user.last_name) for user in result.scalars()]


@router.post("")
async def add_friend_request(
        new_friend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if new_friend_id == user.id:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        result = await session.execute(select(Rs).where(Rs.user_1_id == user.id, Rs.user_2_id == new_friend_id))

        if len(result.all()):
            raise HTTPException(status_code=400, detail="Заявка уже отправлена")

        stmt = insert(Rs).values(user_1_id=user.id, user_2_id=new_friend_id, status_id=2)
        await session.execute(stmt)
        stmt = insert(Rs).values(user_2_id=user.id, user_1_id=new_friend_id, status_id=1)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Пользователю {new_friend_id} отправлена заявка",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception as ex:
        return {
            "status_code": 400,
            "detail": ex.args,
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
            .where(Rs.user_1_id == user.id, Rs.user_2_id == new_friend_id, Rs.status_id == 1)
        result = await session.execute(stmt)

        if not result.rowcount:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        stmt = update(Rs)\
            .values(status_id=3)\
            .where(Rs.user_1_id == new_friend_id, Rs.user_2_id == user.id, Rs.status_id == 2)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Пользователь {new_friend_id} добавлен в друзья",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception as ex:
        return {
            "status_code": 400,
            "detail": ex.args,
            "headers": None
        }


@router.delete("")
async def unfriend(
        unfriend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(Rs).where(Rs.user_1_id == user.id, Rs.user_2_id == unfriend_id, Rs.status_id == 3)
        result = await session.execute(stmt)

        if not result.rowcount:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        stmt = delete(Rs).where(Rs.user_2_id == user.id, Rs.user_1_id == unfriend_id, Rs.status_id == 3)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Пользователь {unfriend_id} удален из друзей",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception as ex:
        return {
            "status_code": 400,
            "detail": ex.args,
            "headers": None
        }


@router.delete("/requests/out")
async def remove_out_request(
        unfriend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(Rs).where(Rs.user_1_id == user.id, Rs.user_2_id == unfriend_id, Rs.status_id == 2)
        result = await session.execute(stmt)

        if not result.rowcount:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        stmt = delete(Rs).where(Rs.user_2_id == user.id, Rs.user_1_id == unfriend_id, Rs.status_id == 1)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Заявка пользователю {unfriend_id} отменена",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception as ex:
        return {
            "status_code": 400,
            "detail": ex.args,
            "headers": None
        }


@router.delete("/requests/in")
async def remove_in_request(
        unfriend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(Rs).where(Rs.user_1_id == user.id, Rs.user_2_id == unfriend_id, Rs.status_id == 1)
        result = await session.execute(stmt)

        if not result.rowcount:
            raise HTTPException(status_code=400, detail="Недопустимое значение")

        stmt = delete(Rs).where(Rs.user_2_id == user.id, Rs.user_1_id == unfriend_id, Rs.status_id == 2)
        await session.execute(stmt)
        await session.commit()

        return {
            "status_code": 201,
            "detail": f"Заявка пользователя {unfriend_id} отклонена",
            "headers": None
        }
    except HTTPException as ex:
        return ex

    except Exception as ex:
        return {
            "status_code": 400,
            "detail": ex.args,
            "headers": None
        }