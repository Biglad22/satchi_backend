from sqlalchemy.orm import Session 
from ..schemas import AvailabilityCheckReq
from sqlalchemy import select
from app.modules.users.models import USER
from fastapi import HTTPException, status

def check_availability_controller(req:AvailabilityCheckReq, db:Session):
    
    response = {}

    def confirm_email():
        refined_email = req.email.strip().lower()
        email_query = select(USER).where(USER.email == refined_email)
        return db.scalar(email_query) 

    def confirm_username():
        refined_name = req.username.strip()
        email_query = select(USER).where(USER.username == refined_name)
        return db.scalar(email_query) 
    
    if not req.username and not req.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username required")
    

    if req.email:
        response["email"] = confirm_email() is None

    if req.username:
        response["username"] = confirm_username() is None


    return response