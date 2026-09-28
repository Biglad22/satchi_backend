from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WriterInBlog(BaseModel):
    id : int
    call_sign : str
    signature: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BlogOut(BaseModel):
    id:int
    title:str
    message: str
    writer_id:int
    writer: WriterInBlog
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)


class NewBlogReq(BaseModel):
    call_sign: str
    message:str
    title:str

class Pagination(BaseModel):
    page: int
    limit: int
    total_pages: int

class AllBlogResponse(BaseModel):
    data: list[BlogOut]
    count: int
    pagination:Pagination
    
    model_config=ConfigDict(from_attributes=True)

class GetUserBlogsReq(BaseModel):
    call_sign: str
