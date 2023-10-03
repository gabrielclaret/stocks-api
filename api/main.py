import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config.logging import RequestIdFilter, RequestIdFormatterHandler
from api.config.settings import get_settings
from api.middlewares.logging import RequestIdLoggingMiddleware
from api.routes import api

LOG_LEVEL = logging.getLevelName("INFO")

app = FastAPI()

settings = get_settings()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def setup_logging() -> None:
    """Configure logging across entire app."""
    loggers = list(logging.root.manager.loggerDict.keys())
    loggers.append("root")
    for name in loggers:
        logger = logging.getLogger(name)
        logger.handlers = [RequestIdFormatterHandler()]
        logger.filters = [RequestIdFilter("request_id")]
        logger.level = LOG_LEVEL
        logger.propagate = False


@app.on_event("startup")
def app_startup_event() -> None:
    """Startup event."""
    setup_logging()


app.add_middleware(RequestIdLoggingMiddleware)
app.include_router(api.endpoint_router, prefix=settings.API_V1_PREFIX)
