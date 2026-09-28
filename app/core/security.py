from typing import Dict
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(data: Dict, life_span:float = 1 ):
    expiry = datetime.now() + timedelta(hours=float(life_span))
    data_copy = data.copy()

    data_copy.update({"exp": int(expiry.timestamp())}) 
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("ALGORITHM")
    return jwt.encode(data_copy, secret, algorithm=algorithm)


def verify_token(token:str) -> int | None:
    try:
        secret = os.getenv("JWT_SECRET")
        algorithm = os.getenv("ALGORITHM")

        data = jwt.decode(token=token, key=secret, algorithms=algorithm)
        user_id = data["id"]
        return user_id
    except ExpiredSignatureError:
        # token has expired
        return None
    except JWTError as error:
        raise error
