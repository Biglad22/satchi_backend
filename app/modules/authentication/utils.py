from fastapi import Response
from app.core.security import create_token
import os
from dotenv import load_dotenv
import random, string
from app.core.redis_client import redis_storage
from datetime import timedelta
load_dotenv()
acc_token_life = os.getenv("ACCESS_TOKEN_LIFE_SPAN")
refresh_token_life = os.getenv("REFRESH_TOKEN_LIFE_SPAN")


def build_msg_for_signing(nonce:str):
    return(
        "Satshi pay authentication \n"
        f"Nonce: {nonce}\n"
    )

#SET ACCESS AND REFRESH TOKENS AS HTTPS COOKIES
def set_access_cookies (res:Response, user_id:str):
    res.set_cookie(
        key="access_token",
        value=create_token({"id":user_id}, life_span=acc_token_life),
        httponly=True,
        samesite="lax",
        max_age= acc_token_life * 60 * 60,
        secure=False
    )

def set_refresh_cookies (res:Response, user_id:str):
    res.set_cookie(
        key="refresh_token",
        value=create_token({"id":user_id}, life_span=refresh_token_life),
        httponly=True,
        samesite="lax",
        max_age= refresh_token_life * 60 * 60 ,
        secure=False
    )

def clear_access_cookies (res:Response):
    res.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False
    )

def clear_refresh_cookies (res:Response):
    res.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax",
        secure=False
    )


def generate_otp(length:int=6):
    return ''.join(random.choices(string.digits, k=length))


def store_otp(email: str, otp:int):
    if not otp or not email: raise Exception("otp and email are required")
    redis_storage.setex(f"otp:{email}", timedelta(minutes=5), otp)

def get_otp(email: str):
    if not email: raise Exception("email is required")
    return  redis_storage.get(f"otp:{email}")

def delete_otp(email: str):
    if not email: raise Exception("email is required")
    redis_storage.delete(f"otp:{email}")

def replace_otp(email: str, otp:int):
    if not otp or not email: raise Exception("otp and email are required")
    delete_otp(email)
    store_otp(email, otp)


