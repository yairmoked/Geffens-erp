from __future__ import annotations

from enum import Enum

from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class BranchType(str, Enum):
    HQ = "HQ"
    SALES = "SALES"
    WAREHOUSE = "WAREHOUSE"
    FACTORY = "FACTORY"


class Company(TimestampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(50))
    base_currency: Mapped[str] = mapped_column(String(3), default="ILS", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    branches: Mapped[list[Branch]] = relationship(back_populates="company")


class Branch(TimestampMixin, Base):
    __tablename__ = "branches"
    __table_args__ = (UniqueConstraint("company_id", "code", name="uq_branches_company_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    branch_type: Mapped[BranchType] = mapped_column(SAEnum(BranchType), default=BranchType.SALES, nullable=False)

    company: Mapped[Company] = relationship(back_populates="branches")


class Currency(TimestampMixin, Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String(5))


class ExchangeRate(TimestampMixin, Base):
    __tablename__ = "exchange_rates"
    __table_args__ = (UniqueConstraint("base_currency", "quote_currency", "rate_date", name="uq_fx_rate_day"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    base_currency: Mapped[str] = mapped_column(ForeignKey("currencies.code"), nullable=False)
    quote_currency: Mapped[str] = mapped_column(ForeignKey("currencies.code"), nullable=False)
    rate_date: Mapped[str] = mapped_column(String(10), nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False)
