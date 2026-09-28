from sqlalchemy.orm import Session
from sqlalchemy import select
from ...users.models import USER
from fastapi import HTTPException, status, Response
from ..utils import clear_access_cookies, clear_refresh_cookies

def sign_out_controller(db:Session, current_user_id:int, response: Response):
    user_search_query = select(USER).where(USER.id == current_user_id)
    current_user = db.scalar(user_search_query)

    if not current_user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    
    clear_refresh_cookies(res=response)
    clear_access_cookies(res=response)

