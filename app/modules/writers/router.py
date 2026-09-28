from fastapi import APIRouter, Depends, status, Query
from ...db.session import get_DB
from json import dump 
from .schemas import GetAllWriterBlog
from .controllers import get_writer as get_writer_controller, get_blogs_by_writer_controller, get_all_writers_controller


WriterRouter = APIRouter(prefix="/writers")

@WriterRouter.get("/", status_code=status.HTTP_200_OK)
def get_all_writers(limit:int=Query(ge=1), page:int=Query(ge=1), db=Depends(get_DB)):
    return get_all_writers_controller(db=db, limit=limit, page=page)


@WriterRouter.get("/{writer_id}", status_code=status.HTTP_200_OK)
def get_writer(writer_id:int,db=Depends(get_DB)):
    return get_writer_controller(writer_id=writer_id, db=db)

@WriterRouter.get("/{writer_id}", response_model=GetAllWriterBlog)
def get_blogs_by_writer (writer_id:int, db=Depends(get_DB)):
    return get_blogs_by_writer_controller(writer_id, db)