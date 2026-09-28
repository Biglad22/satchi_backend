from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import select
from app.modules.users.models import USER
from app.core.hash_password import compare_passwords
from ..schemas import SignInReq
from ..utils import set_refresh_cookies, set_access_cookies

def sign_in_with_credentials_controller(req:SignInReq, response:Response, db:Session):
    req_email = req.email_username.strip()

    if not req_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User email is required") 
    
    email_query = select(USER).where(USER.email == req_email.lower())
    user = db.scalar(email_query)

    if not user:
        username_query = select(USER).where(USER.username == req_email)
        user = db.scalar(username_query)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your login credentials are incorrect.")
    
    password_isValid = compare_passwords(user.hashed_password, req.password)

    if not password_isValid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password is incorrect")
    
    set_access_cookies(res=response, user_id=user.id)
    set_refresh_cookies(res=response, user_id=user.id)
    


    return {"message": "verified", "user" : user}
