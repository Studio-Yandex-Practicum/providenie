from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.auth import get_current_admin

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/admin",
            dependencies=[Depends(get_current_admin)],
            response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
) -> HTMLResponse:
    """Главная страница админки."""
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "title": "Admin Dashboard"},
    )
