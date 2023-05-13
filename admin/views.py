from typing import List

from starlette.requests import Request
from starlette_admin import action
from starlette_admin.contrib.sqlmodel import ModelView

from .models import Edl


class EdlView(ModelView):
    detail_template = 'edl_detail.html'
    actions = ['delete', 'render']

    @action(
        name='render',
        text='Render',
        confirmation='Are you sure?',
        submit_btn_text='Do it!',
    )
    async def render(self, request: Request, edls: List[Edl]) -> str:
        """Render EDL"""
        return f'Rendering {len(edls)} EDLs'
