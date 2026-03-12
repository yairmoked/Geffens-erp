from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class StockBalance(Base):
    __tablename__ = "stock_balances"
    __table_args__ = (UniqueConstraint("company_id", "warehouse_id", "product_id", name="uq_stock_balance_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity_on_hand: Mapped[float] = mapped_column(default=0, nullable=False)
    quantity_reserved: Mapped[float] = mapped_column(default=0, nullable=False)


class StockMove(TimestampMixin, Base):
    __tablename__ = "stock_moves"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    source_warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouses.id"))
    dest_warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouses.id"))
    reference_type: Mapped[str | None] = mapped_column(String(30))
    reference_id: Mapped[int | None] = mapped_column()
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_cost: Mapped[float] = mapped_column(Amount, default=0, nullable=False)


class InventoryAdjustment(TimestampMixin, Base):
    __tablename__ = "inventory_adjustments"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", nullable=False)
