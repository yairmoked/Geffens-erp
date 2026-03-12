from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class MarketplaceIntegration(TimestampMixin, Base):
    __tablename__ = "marketplace_integrations"
    __table_args__ = (UniqueConstraint("company_id", "channel_code", name="uq_company_channel"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    channel_code: Mapped[str] = mapped_column(String(40), nullable=False)  # WOLT/SHOPIFY/etc.
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    base_url: Mapped[str] = mapped_column(String(300), nullable=False)
    api_key: Mapped[str | None] = mapped_column(String(255))
    api_secret: Mapped[str | None] = mapped_column(String(255))
    webhook_secret: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MarketplaceOrder(TimestampMixin, Base):
    __tablename__ = "marketplace_orders"
    __table_args__ = (UniqueConstraint("integration_id", "external_order_id", name="uq_external_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    integration_id: Mapped[int] = mapped_column(ForeignKey("marketplace_integrations.id"), nullable=False)
    external_order_id: Mapped[str] = mapped_column(String(80), nullable=False)
    external_order_no: Mapped[str | None] = mapped_column(String(80))
    customer_name: Mapped[str | None] = mapped_column(String(200))
    customer_phone: Mapped[str | None] = mapped_column(String(30))
    channel_status: Mapped[str] = mapped_column(String(30), default="RECEIVED", nullable=False)
    erp_status: Mapped[str] = mapped_column(String(30), default="PENDING_PICK", nullable=False)
    sales_order_id: Mapped[int | None] = mapped_column(ForeignKey("sales_orders.id"))
    total_amount: Mapped[float] = mapped_column(Amount, default=0, nullable=False)


class MarketplaceOrderLine(Base):
    __tablename__ = "marketplace_order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    marketplace_order_id: Mapped[int] = mapped_column(ForeignKey("marketplace_orders.id"), nullable=False)
    external_line_id: Mapped[str | None] = mapped_column(String(80))
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    external_sku: Mapped[str | None] = mapped_column(String(80))
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    ordered_qty: Mapped[float] = mapped_column(nullable=False)
    picked_qty: Mapped[float] = mapped_column(default=0, nullable=False)
    unit_price: Mapped[float] = mapped_column(Amount, default=0, nullable=False)


class PickingBatch(TimestampMixin, Base):
    __tablename__ = "picking_batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    batch_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="OPEN", nullable=False)
    picker_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class PickingTask(TimestampMixin, Base):
    __tablename__ = "picking_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    picking_batch_id: Mapped[int] = mapped_column(ForeignKey("picking_batches.id"), nullable=False)
    marketplace_order_id: Mapped[int] = mapped_column(ForeignKey("marketplace_orders.id"), nullable=False)
    priority: Mapped[int] = mapped_column(default=100, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="READY", nullable=False)


class PickingTaskLine(Base):
    __tablename__ = "picking_task_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    picking_task_id: Mapped[int] = mapped_column(ForeignKey("picking_tasks.id"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    requested_qty: Mapped[float] = mapped_column(nullable=False)
    picked_qty: Mapped[float] = mapped_column(default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="OPEN", nullable=False)
