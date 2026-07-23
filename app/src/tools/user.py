from datetime import datetime, date

from nicegui import app, ui


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to('/login')


def get_user_name() -> str:
    return app.storage.user.get("username", "Guest")


def str_to_datetime(str_time: str) -> datetime:
    return datetime.fromisoformat(str_time)


def dict_to_datetime(data: dict, key: str) -> datetime:
    return datetime.fromisoformat(data.get(key, datetime.now().isoformat()))


def str_to_date(str_time: str) -> datetime:
    return datetime.fromisoformat(str_time)


def dict_to_date(data: dict, key: str) -> date:
    return date.fromisoformat(data.get(key, date.today().isoformat()))
