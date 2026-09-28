from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException, status
from eth_account.messages import encode_defunct 
from eth_account.account import Account
from uuid import uuid4
from datetime import datetime, timezone
from ..schemas import GetNonceRequest, VerifyWalletRequest
from app.modules.users.models import USER, WalletType
from ..utils import build_msg_for_signing, set_access_cookies, set_refresh_cookies
#SIGNIN WITH WALLET REQUIRES WALLET AUTHENTICATION USING SIGNED MESSAGE
# SEND NONCE FOR SIGNING TO USER 
def send_nonce_controller(req: GetNonceRequest, db:Session): 
    fresh_nonce = uuid4()
    nonce_time = datetime.now(timezone.utc)
    query = select(USER).where(USER.wallet_address == req.wallet_address)
    user = db.scalar(query)
    if user:
        user.nonce = fresh_nonce
        db.commit()
    else:
        user = USER(
            nonce=fresh_nonce,  
            wallet_address=req.wallet_address,
            nonce_issued_at=nonce_time,
            username=req.wallet_address,
            wallet_type=WalletType.NONCUSTODIAL
        )
        db.add(user)
        
    db.commit()
    db.refresh(user)

    response_message = build_msg_for_signing(
        nonce=user.nonce,
    )

    return {
        "message": response_message
    }


# VERIFY SIGNED MESSAGE AND SEND ACCESS TOKENS
def verify_wallet_controller(req : VerifyWalletRequest, response: Response, db:Session):

    query = select(USER).where(USER.wallet_address == req.wallet_address)
    user = db.scalar(query)

    if not user:
        raise HTTPException( detail="User not found" ,status_code=status.HTTP_400_BAD_REQUEST)

    expected_message = build_msg_for_signing(nonce=user.nonce)

    if expected_message != req.message:
        raise HTTPException( detail="Message does not match expectation" ,status_code=status.HTTP_400_BAD_REQUEST)
    
    crypt_msg = encode_defunct(text=req.message)
    recovery =  Account.recover_message(signable_message=crypt_msg, signature=req.signature)

    if not recovery == user.wallet_address:
        raise HTTPException(detail="Wallet unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)
    
    user.isVerified = True
    db.commit()
    db.refresh(user)
    set_access_cookies(res=response, user_id=user.id)
    set_refresh_cookies(res=response, user_id=user.id)

    return {"message": "wallet verified", "user" : user}

