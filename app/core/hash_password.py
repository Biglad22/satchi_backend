from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_ctx.hash(password)

def compare_passwords(hashed_password:str, password:str)->bool:
    isValid = pwd_ctx.verify(password, hashed_password)
    return isValid