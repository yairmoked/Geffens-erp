from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class SalesOrder(TimestampMixin, Base):
    __tablename__ = "sales_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("business_partners.id"), nullable=False)
    order_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", nullable=False)
    currency_code: Mapped[str] = mapped_column(ForeignKey("currencies.code"), nullable=False)
    subtotal: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Amount, default=0, nullable=False)


class SalesOrderLine(Base):
    __tablename__ = "sales_order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    sales_order_id: Mapped[int] = mapped_column(ForeignKey("sales_orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(Amount, nullable=False)
    discount_percent: Mapped[float] = mapped_column(default=0, nullable=False)
    line_total: Mapped[float] = mapped_column(Amount, nullable=False)


class CustomerInvoice(TimestampMixin, Base):
    __tablename__ = "customer_invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    sales_order_id: Mapped[int | None] = mapped_column(ForeignKey("sales_orders.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("business_partners.id"), nullable=False)
    invoice_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", nullable=False)
    total_amount: Mapped[float] = mapped_column(Amount, nullable=False)
