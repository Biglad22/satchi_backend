from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_DB
from .schemas import GetNonceResponse, GetNonceRequest, VerifyWalletRequest, SignInReq, AvailabilityCheckReq, ProfileUpdateReq, MessageResponse, EmailVerificationReq, EmailTokenVerificationReq
from .controllers.sign_in_with_credentials import sign_in_with_credentials_controller
from .controllers.sign_in_with_wallet import send_nonce_controller, verify_wallet_controller
from .schemas import SignUpReq, MessageAndUserRes, AvailabilityCheckRes
from .controllers.sign_up_with_credentials import sign_up_with_credentials_controller
from .controllers.check_availability import check_availability_controller
from .controllers.update_profile import update_profile as update_profile_controller
from .controllers.email_verification import send_email_verification_otp as send_email_verification_otp_controller
from app.core.dependencies.route_guard import route_guard
from .controllers.verify_email_otp import verify_email_otp_controller
from .controllers.sign_out import sign_out_controller

AuthRouter = APIRouter(prefix="/auth")

#SENDS NONCE FOR SIGNING
@AuthRouter.post("/get-nonce", response_model=GetNonceResponse, status_code=status.HTTP_200_OK)
def send_nonce(req: GetNonceRequest, db:Session=Depends(get_DB)):
   return send_nonce_controller(req=req, db=db)

#VERIFY USER WALLET ADDRESS FROM SIGNED NONCE
@AuthRouter.post("/verify-wallet", response_model= MessageAndUserRes, status_code=status.HTTP_201_CREATED)
def verify_wallet(req : VerifyWalletRequest, response: Response, db:Session = Depends(get_DB)):
    return verify_wallet_controller(req=req, response=response, db=db)

# AUTHENTICATE USER WITH EMAIL AND PASSWORD
@AuthRouter.post("/sign-in", response_model= MessageAndUserRes, status_code=status.HTTP_200_OK)
def sign_in_with_credentials(req:SignInReq, response:Response, db:Session = Depends(get_DB)):
    return sign_in_with_credentials_controller(req=req, response=response, db=db)

# CREATE NEW USER WITH CREDENTIALS
@AuthRouter.post("/sign-up", response_model= MessageAndUserRes, status_code=status.HTTP_201_CREATED)
def sign_up_with_credentials(req:SignUpReq, res:Response, db:Session = Depends(get_DB)):
    return sign_up_with_credentials_controller(res=res, req=req, db=db)

#CHECK EMAIL OR USERNAME AVAILABILITY
@AuthRouter.post("/check-availability", response_model=AvailabilityCheckRes, status_code=status.HTTP_200_OK)
def check_availability(req:AvailabilityCheckReq, db:Session=Depends(get_DB)):
    return check_availability_controller(req=req, db=db)


@AuthRouter.patch("/update/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=MessageAndUserRes)
def update_user_profile(user_id:int, req:ProfileUpdateReq, current_user=Depends(route_guard) ,db=Depends(get_DB)):
    return update_profile_controller(req=req, db=db, user_id=user_id, current_user=current_user)

@AuthRouter.post("/send-email-otp", status_code=status.HTTP_200_OK, response_model=MessageResponse)
def request_email_verification(req:EmailVerificationReq,current_user=Depends(route_guard), db:Session =Depends(get_DB)):
    return send_email_verification_otp_controller(current_user_id=current_user, db=db, req_body=req)
    

@AuthRouter.post("/verify-email", status_code=status.HTTP_200_OK, response_model=MessageResponse)
def request_email_verification(req:EmailTokenVerificationReq,current_user=Depends(route_guard), db:Session=Depends(get_DB)):
    return verify_email_otp_controller(current_user_id=current_user, db=db, req_body=req)

@AuthRouter.post("/sign-out", status_code=status.HTTP_200_OK)
def sign_out(res:Response, user_id=Depends(route_guard), db:Session=Depends(get_DB)):
    sign_out_controller(db=db, current_user_id=user_id, response=res)