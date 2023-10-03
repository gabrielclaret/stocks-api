import logging

from starlette_context import context


class RequestIdFilter(logging.Filter):
    """Class for request id filter."""

    def __init__(self, name: str = "") -> None:
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter function."""
        try:
            record.request_id = context.request_id
        except AttributeError:
            pass

        return True


class RequestIdFormatterHandler(logging.StreamHandler):
    """Intercept handler."""

    def format(self, record: logging.LogRecord) -> None:
        """Format the specified record."""
        fmt = logging.Formatter(
            "%(asctime)s | %(request_id)s | %(levelname)s - %(message)s",
            defaults={"request_id": "00000000-0000-0000-0000-000000000042"},
        )
        return fmt.format(record)
