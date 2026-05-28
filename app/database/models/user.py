from datetime import datetime
import enum

from sqlalchemy import Boolean, DateTime, String, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuthStatus(enum.StrEnum):
    ANONYMOUS = "anonymous" # No password and/or email
    UNVERIFIED = "unverified" # Email and password but no email verification
    VERIFIED = "verified" # Email Verified


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    status: Mapped[AuthStatus] = mapped_column(
        Enum(
            AuthStatus,
            name="auth_status",
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        default=AuthStatus.ANONYMOUS,
        server_default=AuthStatus.ANONYMOUS.value,
        nullable=False,
    )