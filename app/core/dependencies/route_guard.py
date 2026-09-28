from fastapi import Request, HTTPException, status, Response
from app.core.security import verify_token
from app.modules.authentication.utils import set_access_cookies

def route_guard(req: Request, res:Response)-> int:
    cookies = req.cookies
    access_token = cookies.get("access_token")
    refresh_token = cookies.get("refresh_token")
    user_id = None


    def use_refresh_token():
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        nonlocal user_id
        user_id = verify_token(refresh_token)
        
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")        
        set_access_cookies(res=res, user_id=user_id)


    if access_token:
        user_id = verify_token(access_token)
        
    if not user_id:
        use_refresh_token()
            
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return user_id
