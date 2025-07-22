import logging
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        method = request.method
        path = request.url.path
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logger.info(f"IP: {ip} | Method: {method} | Path: {path}"
                    f"")

        response = await call_next(request)
        return response
