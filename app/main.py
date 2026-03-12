from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.services.replenishment import ReplenishmentInput, calculate_min_max_order

app = FastAPI(title="Geffens Supermarket ERP")
templates = Jinja2Templates(directory="app/web/templates")


class ReplenishmentPayload(BaseModel):
    available_qty: float
    min_stock: float
    max_stock: float
    safety_stock: float = 0
    order_multiple: float = 1


PAGE_MAP = {
    "dashboard": "דשבורד",
    "procurement": "רכש לסופרמרקט",
    "replenishment": "הזמנות מינימום/מקסימום",
    "commerce_integrations": "התממשקות אתרי סחר",
    "commerce_orders": "הזמנות מאתר סחר",
    "picking": "ליקוט הזמנות",
    "inventory": "מלאי",
    "finance": "כספים",
    "hr": "משאבי אנוש",
}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "pages": PAGE_MAP})


@app.get("/pages/{page_key}", response_class=HTMLResponse)
def module_page(request: Request, page_key: str) -> HTMLResponse:
    page_title = PAGE_MAP.get(page_key, "עמוד לא מוגדר")
    return templates.TemplateResponse(
        "module.html",
        {
            "request": request,
            "page_key": page_key,
            "page_title": page_title,
            "all_pages": PAGE_MAP,
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "geffens-supermarket-erp"}


@app.get("/api/system/mobile-access")
def mobile_access() -> dict[str, str]:
    return {
        "run_command": "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload",
        "browser_url": "http://127.0.0.1:8000",
        "mobile_url_pattern": "http://<YOUR_COMPUTER_LAN_IP>:8000",
        "tip": "ודאי שהמחשב והנייד באותה רשת Wi‑Fi.",
    }


@app.post("/api/replenishment/min-max")
def min_max_replenishment(payload: ReplenishmentPayload) -> dict[str, float | bool]:
    result = calculate_min_max_order(ReplenishmentInput(**payload.model_dump()))
    return {"should_order": result.should_order, "suggested_qty": result.suggested_qty}


@app.get("/api/integrations/channels")
def channels() -> dict[str, list[dict[str, str]]]:
    return {
        "channels": [
            {"code": "shopify", "name": "Shopify"},
            {"code": "wolt", "name": "Wolt"},
            {"code": "woocommerce", "name": "WooCommerce"},
        ]
    }


@app.get("/api/picking/board")
def picking_board() -> dict[str, list[dict[str, str]]]:
    return {
        "tasks": [
            {"order": "WEB-10012", "zone": "A-01", "status": "READY"},
            {"order": "WEB-10013", "zone": "B-03", "status": "PICKING"},
        ]
    }
