# api/main.py


# Lib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from utils.monitoring import PrometheusMiddleware, metrics, setting_otlp

import uvicorn
import logging
import os
import random
import time
import httpx
from typing import Optional
from opentelemetry.propagate import inject

from routers.authenticator import authenticator
from routers.cartographic import cartographic
from routers.information import information
from routers.users import users_router
from routers.tester import tester
from routers.weather import weather

from utils.config import DEBUG, LOGGER, CURRENT_VERSION
from utils.exceptions import CustomException
from utils.limiter import limiter
from utils.logger import SanitizeLoggingMiddleware

APP_NAME = os.environ.get("APP_NAME", "app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

"""
API Declaration
- Disable debug mode in production
"""
app = FastAPI(
    title = "BeeM Project - API module",
    description = "BeeM API module ; Node used to connect UI, Databases and other services",
    version = CURRENT_VERSION,
    openapi_tags = [
    {
        "name": "debug",
        "description": "Debug routes, used to test and debug the API"
    },
    {
        "name": "info",
        "description": "Information routes, used to get information about the API"
    },
    {   
        "name": "auth",
        "description": "Authentication routes, used to login and register users"
    },
    {
        "name": "users",
        "description": "Users routes, used get and update users information"
    },
    {
        "name": "cartographic",
        "description": "Cartographic routes, used to get cartographic data"
    },
    {
        "name": "weather",
        "description": "Weather routes, used to get weather data"
    }
    ],
    debug = DEBUG
    )



"""
Logger Declaration
- Logger is disabled (default), to enable it: Set logger to True in .env file
"""


# Enable middleware if LOGGER is set to True
if LOGGER == "True":
    app.add_middleware(SanitizeLoggingMiddleware)

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

"""
Limiters Declaration
- Limiters are used to limit the number of requests per IP or user_id on the routes
"""
# IP limiter middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code = 429,
    content = {"detail": f"Rate limit exceeded on this route. Rate: {exc.detail}"}
))



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response




"""
Exception Handler
- Custom exception handler used to return custom error messages.
- Custom exceptions are raised in the routers depending the route | name, error_code, message should be defined in the exception
"""

# Exception Handler
@app.exception_handler(CustomException)
def CustomExceptionHandler(request: Request, exception: CustomException):
    return JSONResponse(status_code=exception.error_code,
                        content={
                            "url": str(request.url),
                            "name": exception.name,
                            "message": exception.message,
                            "date": exception.date})




"""
Routers
"""
app.include_router(authenticator)
app.include_router(cartographic)
app.include_router(information)
app.include_router(tester)
app.include_router(users_router)
app.include_router(weather)



"""
Start uvicorn server
"""
if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
