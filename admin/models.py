"""Models

SQLModels for DB and validation
"""

from typing import Any, Dict, List, Optional
from pydantic import AnyHttpUrl, EmailStr, stricturl, datetime_parse
from sqlalchemy import JSON, Column, DateTime, String, Text, Enum
from starlette.requests import Request
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
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


class UserBase(SQLModel):
    """User model

    Attributes:
        id: Primary key
        email: User email
        first_name: User first name
        last_name: User last name
    """

    __tablename__ = 'users'
    email: EmailStr = Field(index=True)
    first_name: str = Field(min_length=1, index=True)
    last_name: Optional[str] = Field(min_length=1, index=True, default=None)

    async def __admin_repr__(self, request: Request):
        return f'{self.first_name} {self.last_name}'


class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)


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

    __tablename__ = 'edls'
    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)
    edl_json: Dict[str, Any] = Field(sa_column=Column(JSON), default=None)

    async def __admin_repr__(self, request: Request):
        return self.name


class Edl(EdlBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)


class Render(SQLModel, table=True):
    """Render model

    Attributes:
        id: Primary key
        status: Render status
        events: List of render events
    """

    __tablename__ = 'renders'
    id: Optional[int] = Field(primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)
    edl: Dict[str, Any] = Field(sa_column=Column(JSON), default=None)
    settings: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    width: int = Field()
    height: int = Field()
    filename: str = Field()
    start_time: datetime = Field(sa_column=Column(DateTime), default=datetime.utcnow)
    end_time: datetime = Field(sa_column=Column(DateTime), default=None)
    # status: AppStatus = Field(sa_column=Enum, default=AppStatus.PENDING)

    async def __admin_repr__(self, request: Request):
        return self.name
