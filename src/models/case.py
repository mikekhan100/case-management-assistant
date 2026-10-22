from datetime import datetime, timezone
import uuid
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.schemas.case import CaseStatus


class CaseModel(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    reference_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[CaseStatus] = mapped_column(
        SQLEnum(CaseStatus), default=CaseStatus.NEW, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    documents: Mapped[list["DocumentModel"]] = relationship(
        "DocumentModel", back_populates="case", cascade="all, delete-orphan"
    )
    summary: Mapped["SummaryModel | None"] = relationship(
        "SummaryModel", back_populates="case", uselist=False, cascade="all, delete-orphan"
    )