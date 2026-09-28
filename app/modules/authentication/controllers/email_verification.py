from ..schemas import EmailVerificationReq
from ...users.models import USER
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from ..utils import generate_otp, replace_otp as redis_replace_otp, get_otp

load_dotenv()

def send_email_verification_otp(req_body:EmailVerificationReq, db:Session, current_user_id:int):
    req_email = req_body.email.strip().lower()
    
    if not req_email: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valid email is required")

    find_user_query = select(USER).where(USER.id == current_user_id)
    user_info = db.scalar(find_user_query)
    
    if not user_info or (not user_info.email == req_email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unrecognized email")

    if user_info.isVerified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already verified")

    verificationToken = get_otp(req_body)

    if verificationToken: 
        raise HTTPException(detail="Verification token is still active. Please wait before requesting a new one.", status_code=status.HTTP_400_BAD_REQUEST)

    otp = generate_otp()

    message = Mail(
        from_email=f"{os.getenv("SENDGRID_SENDER_EMAIL")}",
        to_emails=f"{user_info.email}",
        subject="Email verification",
        html_content=f"""<div style="padding:24px; text-align:center; border-radius:16px; margin:24px; background-color:white;">
          <h3 style="color:black; font-weight:600; padding:8px 0; font-size:24px;">
            Satchi Pay
          </h3>
          <h6 style="color:black; opacity:0.64; font-weight:500; padding:8px 0; font-size:20px;">
            Email Verification
          </h6>
          <h3 style="width:100%; padding:4px 0; color:black; opacity:0.64; font-size:24px;">
            <span>{otp}</span>
          </h3>
          <small style="display:block; font-size:14px; padding-top:8px;">
            Email verification OTP for {user_info.email}
          </small>
        </div>
        """
    )
    sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    sg.send(message)

    redis_replace_otp(req_email, otp)

    return {
        "message" : "Otp successfully sent"
    }
