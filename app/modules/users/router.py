from fastapi import APIRouter, Depends, status
from app.db.session import get_DB
from .controllers.get_user_profile import get_user_profile_controller
from app.core.dependencies.route_guard import route_guard
from app.modules.authentication.schemas import UserOut

UsersRouter = APIRouter()

@UsersRouter.get("/get-me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_profile(db=Depends(get_DB),user_id=Depends(route_guard)):
    return get_user_profile_controller(db=db, current_user_id=user_id)