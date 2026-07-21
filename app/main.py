import os

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import context, ui, app, binding
from starlette.middleware.base import BaseHTTPMiddleware

from src.dtos.user import UserDTO, hash_password
from src.models import UserModel
from src.views.main import main_view


# top-level static routes like /favicon.ico must be unrestricted, otherwise the middleware redirects them to /login
unrestricted_page_routes = {'/favicon.ico', '/login'}


@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if app.storage.user.get('authenticated') or path in unrestricted_page_routes or path.startswith('/_nicegui'):
            return await call_next(request)
        return RedirectResponse(f'/login?redirect_to={path}')


@binding.bindable_dataclass
class UserInfo:
    username: str
    password: str

user_info = UserInfo(username="", password="")


@ui.page('/login')
def login(redirect_to: str = '/') -> RedirectResponse | None:
    if app.storage.user.get('authenticated'):
        return RedirectResponse('/')

    async def try_login() -> None:
        model = UserModel()
        pass_hash = hash_password(password.value or "")
        user: UserDTO | None = await model.get_user(username.value or "user",
                                                    pass_hash)

        if user is not None:
            app.storage.user.update(username=username.value, authenticated=True)
            user_info.username = ""
            user_info.password = ""
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    ui.label("Study Coordinator").classes("text-h2 text-center w-full")

    with ui.card().classes('absolute-center items-stretch'):
        username = ui.input('User name').props('autofocus') \
            .on('keydown.enter', lambda: password.run_method('focus')) \
            .bind_value(user_info, 'username')
        password = ui.input('Password', password=True, password_toggle_button=True) \
            .on('keydown.enter', try_login) \
            .bind_value(user_info, 'password')
        ui.button("Log In", on_click=try_login)

    return None


@ui.page("/")
async def index():
    ui.add_css("""
    .custom-scroll-area .q-scrollarea__content {
        padding: 0px 12px 0px 4px !important;
        gap: 0px !important;
    }
    .edit-view-field .q-field {
        padding-top: 4px !important;
    }
    .small-menu .q-item {
        min-height: 24px;
        padding: 4px 8px;
        font-size: 12px;
    }
    """)

    context.client.content.classes("p-0")
    ui.page_title("Study Coordinator")
    # ui.notify(f"{os.environ.get('SUPABASE_URL', 'MISSING URL')}")
    main_view()


ui.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
    favicon="images/science_24dp_1F1F1F.png",
    title="Study Coordinator",
    reload=True,
    storage_secret=os.environ.get("STORAGE_SECRET", "default_secret"),
)

