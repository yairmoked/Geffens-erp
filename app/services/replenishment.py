from __future__ import annotations

from dataclasses import dataclass
from math import ceil


@dataclass(slots=True)
class ReplenishmentInput:
    available_qty: float
    min_stock: float
    max_stock: float
    safety_stock: float = 0
    order_multiple: float = 1


@dataclass(slots=True)
class ReplenishmentResult:
    should_order: bool
    suggested_qty: float


def calculate_min_max_order(data: ReplenishmentInput) -> ReplenishmentResult:
    """Supermarket-oriented min/max replenishment logic."""
    trigger_level = data.min_stock + data.safety_stock
    target_level = data.max_stock + data.safety_stock
    if data.available_qty >= trigger_level:
        return ReplenishmentResult(should_order=False, suggested_qty=0)

    raw_qty = max(target_level - data.available_qty, 0)
    if data.order_multiple <= 0:
        rounded = raw_qty
    else:
        rounded = ceil(raw_qty / data.order_multiple) * data.order_multiple

    return ReplenishmentResult(should_order=rounded > 0, suggested_qty=rounded)
