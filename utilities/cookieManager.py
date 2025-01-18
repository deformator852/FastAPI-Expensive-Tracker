from fastapi import Request, Response


class CookieManager:
    @staticmethod
    def set_refresh_token(response: Response, refresh_token: str) -> None:
        response.set_cookie(
            key="inventory_app_refresh",
            value=refresh_token,
            httponly=True,
            max_age=15 * 86400,
        )

    @staticmethod
    def get_refresh_token(request: Request) -> str | None:
        return request.cookies.get("inventory_app_refresh")

    @staticmethod
    def delete_refresh_token(response: Response) -> None:
        response.delete_cookie(key="inventory_app_refresh")
