"""App

Main application"""

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.sqlmodel import ModelView, Admin
from sqlmodel import SQLModel

from .models import User, Edl, Render
from ._version import __version__
from .db import engine


def init_database() -> None:
    import admin.models  # noqa: F401

    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title='Alfred',
    version=__version__,
    routes=[
        Route(
            '/',
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[init_database],
)

# Create admin
admin = Admin(engine, title='Alfred')

# Add views
admin.add_view(ModelView(User, icon='fa fa-users'))
admin.add_view(ModelView(Edl, icon='fa fa-file-video'))
admin.add_view(ModelView(Render, icon='fa fa-file-video'))

# Mount to admin to app
admin.mount_to(app)
