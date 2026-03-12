from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class PurchaseOrder(TimestampMixin, Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("business_partners.id"), nullable=False)
    warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouses.id"))
    po_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", nullable=False)
    currency_code: Mapped[str] = mapped_column(ForeignKey("currencies.code"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Amount, nullable=False)
    is_auto_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_cost: Mapped[float] = mapped_column(Amount, nullable=False)
    line_total: Mapped[float] = mapped_column(Amount, nullable=False)


class VendorBill(TimestampMixin, Base):
    __tablename__ = "vendor_bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("business_partners.id"), nullable=False)
    purchase_order_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_orders.id"))
    bill_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="OPEN", nullable=False)
    total_amount: Mapped[float] = mapped_column(Amount, nullable=False)


class SupplierProduct(TimestampMixin, Base):
    """Supplier catalog for supermarket purchasing."""

    __tablename__ = "supplier_products"
    __table_args__ = (
        UniqueConstraint("company_id", "vendor_id", "product_id", name="uq_supplier_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("business_partners.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    vendor_sku: Mapped[str | None] = mapped_column(String(60))
    lead_time_days: Mapped[int] = mapped_column(default=1, nullable=False)
    min_order_qty: Mapped[float] = mapped_column(default=1, nullable=False)
    case_pack_qty: Mapped[float] = mapped_column(default=1, nullable=False)
    latest_cost: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
    is_preferred: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ReplenishmentRule(TimestampMixin, Base):
    """Min/Max inventory rule per product + warehouse."""

    __tablename__ = "replenishment_rules"
    __table_args__ = (
        UniqueConstraint("company_id", "warehouse_id", "product_id", name="uq_replenishment_rule"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    preferred_vendor_id: Mapped[int | None] = mapped_column(ForeignKey("business_partners.id"))
    min_stock: Mapped[float] = mapped_column(default=0, nullable=False)
    max_stock: Mapped[float] = mapped_column(default=0, nullable=False)
    safety_stock: Mapped[float] = mapped_column(default=0, nullable=False)
    order_multiple: Mapped[float] = mapped_column(default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ReplenishmentSuggestion(TimestampMixin, Base):
    __tablename__ = "replenishment_suggestions"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    vendor_id: Mapped[int | None] = mapped_column(ForeignKey("business_partners.id"))
    available_qty: Mapped[float] = mapped_column(default=0, nullable=False)
    suggested_qty: Mapped[float] = mapped_column(default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="NEW", nullable=False)
