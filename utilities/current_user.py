from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.service import UsersService

user_service = UsersService()
security = HTTPBearer()


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    user_id = user_service.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return user_id
