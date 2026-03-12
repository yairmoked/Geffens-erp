from app.models import Base
from app.services.replenishment import ReplenishmentInput, calculate_min_max_order


def test_essential_tables_exist() -> None:
    tables = Base.metadata.tables
    expected = {
        "companies",
        "users",
        "products",
        "purchase_orders",
        "replenishment_rules",
        "replenishment_suggestions",
        "marketplace_integrations",
        "marketplace_orders",
        "picking_batches",
        "picking_tasks",
    }
    assert expected.issubset(set(tables.keys()))


def test_min_max_replenishment_rounding() -> None:
    result = calculate_min_max_order(
        ReplenishmentInput(
            available_qty=3,
            min_stock=8,
            max_stock=20,
            safety_stock=2,
            order_multiple=6,
        )
    )
    assert result.should_order is True
    assert result.suggested_qty == 24


def test_min_max_replenishment_no_order() -> None:
    result = calculate_min_max_order(
        ReplenishmentInput(
            available_qty=15,
            min_stock=8,
            max_stock=20,
            safety_stock=2,
            order_multiple=6,
        )
    )
    assert result.should_order is False
    assert result.suggested_qty == 0
