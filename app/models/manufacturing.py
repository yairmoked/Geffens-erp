from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class BillOfMaterial(TimestampMixin, Base):
    __tablename__ = "bill_of_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)


class BillOfMaterialLine(Base):
    __tablename__ = "bill_of_material_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    bom_id: Mapped[int] = mapped_column(ForeignKey("bill_of_materials.id"), nullable=False)
    component_product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    scrap_percent: Mapped[float] = mapped_column(default=0, nullable=False)


class WorkOrder(TimestampMixin, Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    work_order_no: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    planned_qty: Mapped[float] = mapped_column(nullable=False)
    produced_qty: Mapped[float] = mapped_column(default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="PLANNED", nullable=False)
    standard_cost: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
