import uuid


def get_request_id(original_id: str = "") -> str:
    """Get a new request id.

    If an original_id is provided, it concatenates the original and a new one:
    {original_id}, {new_id}
    """
    new_id = uuid.uuid4()

    if original_id:
        new_id = f"{original_id}, {new_id}"

    return new_id
