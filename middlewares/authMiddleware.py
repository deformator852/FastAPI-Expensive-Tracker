from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import ExpiredSignatureError, JWTError, jwt


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=403, detail="Missing Authorization header")
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer") else None
        if not token:
            raise HTTPException(
                status_code=403, detail="Invalid Authorization header format"
            )

        try:
            payload = jwt.decode(token, "SADSADADADADDADSADMASDA", algorithms=["HS256"])
            user_id = payload.get("user")
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token")
        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")

        request.state.user_id = user_id

        response = await call_next(request)
        return response
