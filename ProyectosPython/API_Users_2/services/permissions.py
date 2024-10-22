from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.models.user import RoleEnum, User
from routers.auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.R_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource"
        )
    return current_user

def get_current_regular_user(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.R_USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource"
        )
    return current_user