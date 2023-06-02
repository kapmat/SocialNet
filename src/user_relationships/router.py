from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from user_relationships.models import *
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
    query = select(Relationship.another_user_id)\
        .where(Relationship.user_id == user.id, Relationship.status_id == 3)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/requests/out")
async def get_friend_out_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Relationship.another_user_id)\
        .where(Relationship.user_id == user.id,  Relationship.status_id == 2)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/requests/in")
async def get_friend_in_requests(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Relationship.another_user_id)\
        .where(Relationship.user_id == user.id,  Relationship.status_id == 1)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("")
async def add_friend_request(
        new_friend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # new_friend_id != user.id
        stmt = insert(Relationship)\
            .values(user_id=user.id, another_user_id=new_friend_id, status_id=2)
        await session.execute(stmt)
        stmt = insert(Relationship)\
            .values(user_id=new_friend_id, another_user_id=user.id, status_id=1)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": 201
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": 500
        })


@router.patch("")
async def add_friend(
        new_friend_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = update(Relationship)\
        .values(status_id=3)\
        .where(Relationship.user_id == user.id, Relationship.another_user_id == new_friend_id)
    await session.execute(stmt)
    stmt = update(Relationship)\
        .values(status_id=3)\
        .where(Relationship.user_id == new_friend_id, Relationship.another_user_id == user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": 201}