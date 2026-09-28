from fastapi import APIRouter
from .api_v1.routes import Api_v1

Api = APIRouter(prefix="/api")
Api.include_router(Api_v1)