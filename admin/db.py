from sqlalchemy import create_engine

from admin.config import DB_URL, DEBUG

engine = create_engine(DB_URL, connect_args={'check_same_thread': False}, echo=DEBUG)


# TODO: implement async engine
def create_async_engine():
    from sqlmodel.ext.asyncio.session import AsyncEngine

    return AsyncEngine(engine)
