# api/utils/logger.py


# Lib
from fastapi import Request
import logging
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
import urllib.parse


from utils.config import LOG_FILE_PATH


"""
Create logging object and configuration
"""

# File handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)

# Logging formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api logger")
logger.addHandler(file_handler)



"""
Create middleware to sanitize sensitive information
- Avoid logging sensitive information such as passwords
"""

class SanitizeLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract client IP
        client_ip = request.client.host

        # Extract request body
        body = await request.body()
        body_str = body.decode("utf-8")

        # Sanitize sensitive information
        sanitized_body_str = self.sanitize_body(body_str)

        # Log sanitized request details
        logger.info(f"Request: {request.method} {request.url} from {client_ip} with body: {sanitized_body_str}")

        try:
            # Process request
            response = await call_next(request)
        except Exception as e:
            # Log exception details
            logger.error(f"Exception occurred: {str(e)}")
            logger.error(traceback.format_exc())
            raise e

        # Log response status
        logger.info(f"Response status: {response.status_code}\n")
        return response

    def sanitize_body(self, body_str: str) -> str:
        # Parse the body string into a dictionary
        parsed_body = urllib.parse.parse_qs(body_str)

        # Replace the value of the "password" key with asterisks
        if "password" in parsed_body:
            parsed_body["password"] = ["********"]
        if "new_password" in parsed_body:
            parsed_body["new_password"] = ["********"]
        if "current_password" in parsed_body:
            parsed_body["current_password"] = ["********"]

        # Recompose the body string
        sanitized_body_str = urllib.parse.urlencode(parsed_body, doseq=True)
        return sanitized_body_str