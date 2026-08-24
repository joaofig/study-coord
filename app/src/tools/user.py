from datetime import date, datetime

from nicegui import app, ui


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


def get_user_name() -> str:
    try:
        return app.storage.user.get("username", "user")
    except RuntimeError:
        return "user"


def str_to_datetime(str_time: str) -> datetime:
    return datetime.fromisoformat(str_time)


def dict_to_datetime(data: dict, key: str,
                     default: datetime | None = None) -> datetime:
    """
    Convert a dictionary value to a datetime.

    Args:
        data: The dictionary containing the value.
        key: The key to look up in the dictionary.
        default: The default value to return if the key is not found or the value is invalid.

    Returns:
        The corresponding datetime or the default value.
    """
    value = data.get(key)
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    elif isinstance(value, datetime):
        return value
    elif default is None:
        raise ValueError(f"Invalid value for key '{key}': {value}")
    else:
        return default


def str_to_date(str_time: str) -> date:
    return date.fromisoformat(str_time)


def dict_to_date(data: dict, key: str,
                 default: date | None = None) -> date | None:
    """
    Convert a dictionary value to a date.

    Args:
        data: The dictionary containing the value.
        key: The key to look up in the dictionary.
        default: The default value to return if the key is not found or the value is invalid.

    Returns:
        The corresponding date or the default value.
    """
    value = data.get(key)
    if isinstance(value, str):
        return date.fromisoformat(value)
    elif isinstance(value, date):
        return value
    else:
        return default
