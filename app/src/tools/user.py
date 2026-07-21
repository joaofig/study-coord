from nicegui import app, ui


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to('/login')
