from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Amount, Base, TimestampMixin


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("company_id", "code", name="uq_account_company_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_control: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class FiscalPeriod(Base):
    __tablename__ = "fiscal_periods"
    __table_args__ = (UniqueConstraint("company_id", "name", name="uq_period_company_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[str] = mapped_column(String(10), nullable=False)
    end_date: Mapped[str] = mapped_column(String(10), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class JournalEntry(TimestampMixin, Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    journal_code: Mapped[str] = mapped_column(String(10), nullable=False)
    document_no: Mapped[str] = mapped_column(String(30), nullable=False)
    posting_date: Mapped[str] = mapped_column(String(10), nullable=False)
    memo: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="POSTED", nullable=False)


class JournalEntryLine(Base):
    __tablename__ = "journal_entry_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    partner_id: Mapped[int | None] = mapped_column(ForeignKey("business_partners.id"))
    debit: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
    credit: Mapped[float] = mapped_column(Amount, default=0, nullable=False)
