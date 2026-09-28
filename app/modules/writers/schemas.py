from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BlogInWriter (BaseModel):
    id:int
    title:str
    message: str
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class WriterOut(BaseModel):
    id : int
    call_sign : str
    signature: str
    created_at: datetime
    blogs: list[BlogInWriter]
    model_config = ConfigDict(from_attributes=True)

class GetAllWriterBlog(BaseModel):
    data: list[BlogInWriter]
    count:int

class GetAllWriters(BaseModel):
    id : int
    call_sign : str
    signature: str
    created_at: datetime
    blogs_count: int

    model_config = ConfigDict(from_attributes=True)