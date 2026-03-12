from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class BusinessPartner(TimestampMixin, Base):
    __tablename__ = "business_partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    partner_type: Mapped[str] = mapped_column(String(20), nullable=False)  # CUSTOMER / VENDOR / BOTH
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    tax_id: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Warehouse(TimestampMixin, Base):
    __tablename__ = "warehouses"
    __table_args__ = (UniqueConstraint("company_id", "code", name="uq_wh_company_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    branch_id: Mapped[int | None] = mapped_column(ForeignKey("branches.id"))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)


class ProductCategory(TimestampMixin, Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("product_categories.id"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    parent: Mapped[ProductCategory | None] = relationship(remote_side=[id])


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("product_categories.id"))
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    uom: Mapped[str] = mapped_column(String(20), default="UNIT", nullable=False)
    product_type: Mapped[str] = mapped_column(String(20), default="STOCK", nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False, default=0)
    cost_price: Mapped[float] = mapped_column(nullable=False, default=0)
    description: Mapped[str | None] = mapped_column(Text)
