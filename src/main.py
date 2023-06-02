from fastapi import FastAPI
from auth.router import router as auth_router
from user_relationships.router import router as friends_router

app = FastAPI(
    title='SocialNet'
)


app.include_router(auth_router)
app.include_router(friends_router)


