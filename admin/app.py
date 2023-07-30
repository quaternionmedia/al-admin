"""App

Main application"""

from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.sqlmodel import Admin, ModelView

from ._version import __version__
from .auth import OAuthProvider
from .config import SECRET
from .db import engine
from .models import Edl, Render, User
from .views import EdlView


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
admin = Admin(
    engine,
    title='Alfred',
    auth_provider=OAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET)],
)


# Add views
admin.add_view(ModelView(User, icon='fa fa-users'))
admin.add_view(EdlView(Edl, icon='fa fa-file-video'))
admin.add_view(ModelView(Render, icon='fa fa-file-video'))

# Mount to admin to app
admin.mount_to(app)
