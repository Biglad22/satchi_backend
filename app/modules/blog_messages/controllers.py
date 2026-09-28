from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from .schemas import NewBlogReq
from .models import Blog
from app.modules.writers.models import Writer
import math


def get_all_blog_controller (page:int, limit:int, db:Session):

    offset = limit * (page - 1)

    stmt = select(Blog).options(joinedload(Blog.writer))    
    total_stmt = select(func.count(Blog.id)).select_from(stmt.subquery())
    total = db.scalar(total_stmt) or 0
    
    stmt= stmt.order_by(Blog.created_at.desc()).offset(offset).limit(limit)
    blogs = db.scalars(stmt).all()

    return{
        "data":blogs,
        "count": total,
        "pagination":{
            "page": int(page),
            "limit" : int(limit),
            "total_pages": max(1, int(math.ceil(total / limit)))
        }
    }

def get_blog_by_id_controller (blog_id:int, db:Session):
    stmt = select(Blog).where(Blog.id == blog_id).options(selectinload(Blog.writer))
    blog = db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog with id not found")
    return blog


def add_new_blog (req:NewBlogReq, db:Session):
    call_sign = req.call_sign.strip()
    
    ## NEW BLOG
    new_blog = Blog(**req.model_dump(exclude={"call_sign"}))

    ## WRITER QUERY
    writer_query_stmt = select(Writer).where(Writer.call_sign == call_sign)
    writer = db.scalar(writer_query_stmt)

    if not writer:
        writer = Writer(call_sign = call_sign)
        db.add(writer)

    writer.blogs.append(new_blog)
    db.commit()
    
    return new_blog
