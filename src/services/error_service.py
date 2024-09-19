from aiohttp import web
from src.schemas.status_response import StatusResponse


class ErrorService:

    @staticmethod
    def handle_error(exception: Exception) -> web.Response:
        match exception:
            case ValueError() | KeyError():
                return ErrorService.handle_400()
            case PermissionError():
                return ErrorService.handle_401()
            case web.HTTPForbidden():
                return ErrorService.handle_403()
            case web.HTTPNotFound():
                return ErrorService.handle_404()
            case _:
                return ErrorService.handle_500()

    @staticmethod
    def handle_400() -> web.Response:
        error_response = StatusResponse(status="error", message="Invalid data format")
        return web.json_response(error_response.dict(), status=400)

    @staticmethod
    def handle_401() -> web.Response:
        error_response = StatusResponse(status="error", message="Unauthorized access")
        return web.json_response(error_response.dict(), status=401)

    @staticmethod
    def handle_403() -> web.Response:
        error_response = StatusResponse(
            status="error", message="Forbidden: Access is denied"
        )
        return web.json_response(error_response.dict(), status=403)

    @staticmethod
    def handle_404() -> web.Response:
        error_response = StatusResponse(status="error", message="Resource not found")
        return web.json_response(error_response.dict(), status=404)

    @staticmethod
    def handle_500() -> web.Response:
        return web.Response(status=500, text="Internal Server Error")
