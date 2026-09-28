from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime

class WalletType(str, Enum):
    CUSTODIAL = "custodial"
    NONCUSTODIAL = "noncustodial"


class UserOut(BaseModel):
    id: int
    wallet_address: Optional[str]
    email: Optional[str]
    username: str
    profile_image: Optional[str]
    created_at: datetime
    updated_at: datetime
    isVerified: bool
    wallet_type: WalletType

    model_config = ConfigDict(from_attributes=True)

class GetNonceResponse(BaseModel):
    message: str
    model_config = ConfigDict(from_attributes=True)

class GetNonceRequest(BaseModel):
    wallet_address: str
    model_config = ConfigDict(from_attributes=True)


class VerifyWalletRequest(BaseModel):
    wallet_address: str
    message: str
    signature: str

    model_config = ConfigDict(from_attributes=True)


class SecurityTokens(BaseModel):
    access_token: str
    refresh_token: str
    
    model_config = ConfigDict(from_attributes=True)


class SignInReq(BaseModel):

    email_username:str
    password:str

    model_config = ConfigDict(from_attributes=True)


class MessageAndUserRes(BaseModel):
    message:str
    user:UserOut
    model_config = ConfigDict(from_attributes=True)


class SignUpReq(BaseModel):
    email:str
    username:str
    password:str
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message:str

    model_config = ConfigDict(from_attributes=True)


class AvailabilityCheckReq(BaseModel):
    email:str | None = None
    username:str | None = None

    model_config = ConfigDict(from_attributes=True)

class AvailabilityCheckRes(BaseModel):
    email:bool | None = None
    username:bool |None = None

    model_config = ConfigDict(from_attributes=True)

class ProfileUpdateReq(BaseModel):
    email: str | None = None
    username: str | None = None

    model_config = ConfigDict(from_attributes=True)

class EmailVerificationReq(BaseModel):
    email:str
    model_config =ConfigDict(from_attributes=True)

class EmailTokenVerificationReq(BaseModel):
    email:str
    otp:int
    model_config =ConfigDict(from_attributes=True)

