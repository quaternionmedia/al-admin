"""Models

SQLModels for DB and validation
"""

from typing import Any, Dict, Optional, List
from pydantic import EmailStr, stricturl
from sqlalchemy import JSON, Column, DateTime, Enum
from starlette.requests import Request
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

MediaUrl = stricturl(allowed_schemes=['video', 'audio', 'text'], tld_required=False)
"""Media url validator. Must have prefix of video, audio, or text. No TLD required.
Example:
    video://*
"""


class AppStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETE = 'complete'
    FAILED = 'failed'


class UserEdlLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        foreign_key='users.id', primary_key=True, default=None
    )
    edl_id: Optional[int] = Field(foreign_key='edls.id', primary_key=True, default=None)


class EdlRenderLink(SQLModel, table=True):
    edl_id: Optional[int] = Field(foreign_key='edls.id', primary_key=True, default=None)
    render_id: Optional[int] = Field(
        foreign_key='renders.id', primary_key=True, default=None
    )


class UserBase(SQLModel):
    """User model

    Attributes:
        id: Primary key
        email: User email
        first_name: User first name
        last_name: User last name
    """

    email: EmailStr = Field(index=True)
    first_name: str = Field(min_length=1, index=True)
    last_name: Optional[str] = Field(min_length=1, index=True, default=None)

    async def __admin_repr__(self, request: Request):
        return f'{self.first_name} {self.last_name}'


class User(UserBase, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(primary_key=True, default=None)
    edls: List['Edl'] = Relationship(back_populates='user', link_model=UserEdlLink)


class UserCreate(UserBase):
    pass


class EdlBase(SQLModel):
    """EDL model

    Attributes:
        id: Primary key
        name: EDL name
        description: EDL description
        edl_json: JSON representation of the EDL
    """

    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)
    edl: Dict[str, Any] = Field(sa_column=Column(JSON), default=None)

    async def __admin_repr__(self, request: Request):
        return self.name


class Edl(EdlBase, table=True):
    __tablename__ = 'edls'
    id: Optional[int] = Field(primary_key=True, default=None)
    user_id: Optional[int] = Field(foreign_key='users.id', default=None)
    user: User = Relationship(back_populates='edls', link_model=UserEdlLink)
    renders: List['Render'] = Relationship(
        back_populates='edl', link_model=EdlRenderLink
    )


class RenderBase(SQLModel):
    """Render model

    Attributes:
        id: Primary key
        status: Render status
        events: List of render events
    """

    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)

    settings: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    width: int = Field()
    height: int = Field()
    filename: str = Field(index=True)
    start_time: Optional[datetime] = Field(
        sa_column=Column(DateTime), default=datetime.utcnow
    )
    end_time: Optional[datetime] = Field(sa_column=Column(DateTime), default=None)
    status: str = Field(sa_column=AppStatus, default=None)

    async def __admin_repr__(self, request: Request):
        return self.name


class Render(RenderBase, table=True):
    __tablename__ = 'renders'
    id: Optional[int] = Field(primary_key=True)
    edl_id: Optional[int] = Field(foreign_key='edls.id', default=None)
    edl: Edl = Relationship(back_populates='renders', link_model=EdlRenderLink)
