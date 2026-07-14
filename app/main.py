import os

from nicegui import context, ui

from src.db.sqlite import initialize_database
from src.views.main import main_view


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
    main_view()


def setup_app():
    initialize_database()
    # locator = ResourceLocator()
    # locator["TripModel"] = TripModel()


setup_app()
ui.run(
    host=os.getenv("NICEGUI_HOST"),
    port=int(os.getenv("NICEGUI_PORT", "8080")),
    favicon="images/science_24dp_1F1F1F.png",
    title="Study Coordinator",
    reload=False,
)

