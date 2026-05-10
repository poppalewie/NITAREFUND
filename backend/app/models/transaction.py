from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Text, Enum, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import TransactionType, TransactionStatus

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    lender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    borrower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # 💡 Use Numeric for money (no float bugs)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), default=TransactionType.monetary
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.pending, index=True
    )

    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    settled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

# Indexes for performance
Index("idx_tx_lender", Transaction.lender_id)
Index("idx_tx_borrower", Transaction.borrower_id)
Index("idx_tx_status", Transaction.status)