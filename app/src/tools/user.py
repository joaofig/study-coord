from datetime import date, datetime

from nicegui import app, ui


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


def get_user_name() -> str:
    return app.storage.user.get("username", "user")


def str_to_datetime(str_time: str) -> datetime:
    return datetime.fromisoformat(str_time)


def dict_to_datetime(data: dict, key: str,
                     default: datetime | None = datetime.now()) -> datetime:
    value = data.get(key)
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    elif isinstance(value, datetime):
        return value
    elif default is None:
        raise ValueError(f"Invalid value for key '{key}': {value}")
    else:
        return default


def str_to_date(str_time: str) -> datetime:
    return datetime.fromisoformat(str_time)


def dict_to_date(data: dict, key: str,
                 default: date | None = date.today()) -> date | None:
    value = data.get(key)
    if isinstance(value, str):
        return date.fromisoformat(value)
    elif isinstance(value, date):
        return value
    else:
        return default
