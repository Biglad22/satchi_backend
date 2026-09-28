from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from .models import Writer
from app.modules.blog_messages.models import Blog
import math

def get_all_writers_controller (limit:int, page:int, db:Session):

    offset = limit * (page - 1)
    stmt = select(Writer.id, Writer.call_sign, Writer.created_at.label("join_at"), func.count(Blog.id).label("blog_count")).outerjoin(Blog, Blog.writer_id == Writer.id).group_by(Writer.id).order_by(desc("blog_count")).offset(offset).limit(limit)
    list  = db.execute(statement=stmt).all()

    total_stmt = select(func.count(Writer.id))
    total = db.scalar(total_stmt)

    complete_list = [
        {
            "id": id, 
            "joined_at": joined_at, 
            "call_sign" :call_sign,
            "blog_count" : blog_count
        } for id, call_sign, joined_at, blog_count in list
    ]

    return {
        "data":complete_list,
        "pagination":{
            "page": int(page),
            "limit" : int(limit),
            "total_pages": max(1, int(math.ceil(total / limit)))
        }
    }

def get_writer(writer_id:int, db:Session):

    if not writer_id: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="call_sign is missing from request")
    
    stmt = select(Writer).options(selectinload(Writer.blogs)).where(Writer.id == writer_id)
    writer = db.scalar(stmt)

    if not writer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer does not exist")
    
    return writer


def get_blogs_by_writer_controller(writer_id:int, db:Session):
    stmt = select(Writer).where(Writer.id == writer_id).options(selectinload(Writer.blogs))
    writer = db.scalar(stmt)

    if not writer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="writer not found")

    return {
        "data": writer.blogs,
        "count": len(writer.blogs)
    }