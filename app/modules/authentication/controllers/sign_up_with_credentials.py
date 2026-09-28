from sqlalchemy.orm import Session
from ..schemas import SignUpReq
from fastapi import HTTPException, status, Response
from app.modules.users.models import USER
from app.core.hash_password import hash_password
from sqlalchemy import select
from ..utils import set_access_cookies, set_refresh_cookies


#CREATE USER WALLET


#SIGN UP WITH USER CREDENTIALS
def sign_up_with_credentials_controller(res :Response, req:SignUpReq, db:Session):
    refined_email = req.email.strip().lower()

    if not refined_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email required for signup")
    
    email_query = select(USER).where(USER.email == refined_email)
    user_with_email = db.scalar(email_query)

    user_name_query = select(USER).where(USER.username == req.username)
    user_with_user_name = db.scalar(user_name_query)

    if user_with_email  or user_with_user_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist, sign in")
    
    hashed_password = hash_password(req.password)
    new_user = USER(email=refined_email, hashed_password=hashed_password, username=req.username)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    set_access_cookies(res=res, user_id=new_user.id)
    set_refresh_cookies(res=res, user_id=new_user.id)
    
    return {"message":"user created", "user": new_user}


