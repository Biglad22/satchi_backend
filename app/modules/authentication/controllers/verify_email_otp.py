from ..schemas import EmailTokenVerificationReq
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from ..utils import get_otp, delete_otp
from ...users.models import USER

def verify_email_otp_controller(req_body:EmailTokenVerificationReq, current_user_id:int, db:Session):
    user_email = req_body.email.strip().lower()
    user_otp = req_body.otp

    user_search_query = select(USER).where(USER.id == current_user_id)
    cur_user_info = db.scalar(user_search_query)
    print(user_email)
    if not user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valid email is required for verification")
    
    if not cur_user_info.email == user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unknown email")    

    stored_otp = int(get_otp(user_email) or 0)
    if not user_otp == stored_otp:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid verification token")

    cur_user_info.isVerified = True
    
    db.commit()
    delete_otp(user_email)
    return {
        "message":"email verified",
    }



    
