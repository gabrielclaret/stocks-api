from typing import Any, Dict, Optional, Union

from fastapi import HTTPException

ErrorDetail = Optional[Union[str, Dict[str, str]]]


def raise_error_response(
    error: Union[Any, BaseException],
    detail: ErrorDetail = None,
    **args: Dict[str, Any],
) -> None:
    """Raise a HTTPException with a custom error."""
    error_body = dict(error.error)

    if detail is not None:
        error_body["detail"] = detail

    if args:
        error_body = {**error_body, **args}

    raise HTTPException(
        status_code=error.status_code,
        detail=error_body,
    )


class ErrorInvalidResource:
    """Class that defines an error for an invalid resource."""

    status_code = 400

    error = {
        "type": "invalid_resource",
        "description": "The requested resource is invalid.",
    }


class ErrorInvalidQueryParameters:
    """Class that defines an error for an invalid query parameter."""

    status_code = 400

    error = {
        "type": "invalid_query_parameters",
        "description": "The request has invalid query parameters.",
    }


class ErrorInternal:
    """Class that defines an error for an internal error."""

    status_code = 500

    error = {
        "type": "internal_error",
        "description": "An internal error has occurred "
        "while processing the request.",
    }


class NotFound:
    """Class that defines an error for a not found resource."""

    status_code = 404

    error = {
        "type": "not_found",
        "description": "The server can not find the requested resource.",
    }
