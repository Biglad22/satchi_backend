from fastapi import APIRouter, status,Depends, Query
from ...db.session import get_DB
from .schemas import NewBlogReq, BlogOut, AllBlogResponse
from .controllers import add_new_blog, get_all_blog_controller, get_blog_by_id_controller

Blog_messages_router = APIRouter(prefix="/blogs")

@Blog_messages_router.get("", status_code=status.HTTP_200_OK, response_model=AllBlogResponse)
def get_all_blogs(page:int=Query(1, ge=1), limit:int=Query(10, ge=1), db=Depends(get_DB)):
    return get_all_blog_controller(page=page, limit=limit, db=db)

@Blog_messages_router.post("", status_code=status.HTTP_201_CREATED, response_model=BlogOut)
def create_blog(req:NewBlogReq, db=Depends(get_DB)):
    return add_new_blog(req, db)

@Blog_messages_router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=BlogOut)
def get_blog_by_id(blog_id:int, db=Depends(get_DB)):
    return get_blog_by_id_controller(blog_id, db)
