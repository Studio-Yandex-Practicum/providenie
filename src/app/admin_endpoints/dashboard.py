from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')
router = APIRouter()


@router.get('/admin', response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
) -> HTMLResponse:
    """Главная страница админки."""
    return templates.TemplateResponse(
        'admin_dashboard.html',
        {'request': request, 'title': 'Admin Dashboard'},
    )
