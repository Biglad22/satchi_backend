from sqlalchemy.orm import Session
from sqlalchemy import update
from ..controllers import update_profile as update_profile_req 
from fastapi import HTTPException, status
from app.modules.users.models import USER
def update_profile(db:Session, current_user:int, req:update_profile_req, user_id:int):
    
    print(current_user, user_id)

    if not current_user == user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized, invalid user")

    query = update(USER).where(USER.id == user_id).values(**req.__dict__).returning(USER)
    updated_user = db.scalar(query)

    if not updated_user: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()

    return {
        "message":"Profile successfully updated",
        "user":updated_user
    }
