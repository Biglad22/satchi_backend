from app.modules.blog_messages.router import Blog_messages_router
from fastapi import APIRouter
from app.modules.users.router import UsersRouter
from app.modules.authentication.router import AuthRouter
from app.modules.writers.router import WriterRouter

Api_v1 = APIRouter(prefix="/v1")

Api_v1.include_router(UsersRouter)
Api_v1.include_router(AuthRouter)
Api_v1.include_router(WriterRouter)
Api_v1.include_router(Blog_messages_router)