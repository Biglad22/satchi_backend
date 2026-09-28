from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import USER

def get_user_profile_controller(db:Session, current_user_id:int):
    
    user_search_query = select(USER).where(USER.id == current_user_id)
    user = db.scalar(user_search_query)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

