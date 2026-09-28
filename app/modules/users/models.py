from ...db.database import Base
from sqlalchemy import func, DateTime, String, Integer, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from enum import Enum as PythonEnum

class WalletType(PythonEnum):
    CUSTODIAL = "custodial"
    NONCUSTODIAL = "noncustodial"

class USER(Base):
    __tablename__="users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    isVerified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    wallet_address : Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    email : Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    username : Mapped[str] = mapped_column(unique=True)
    profile_image : Mapped[str | None] = mapped_column(String, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    nonce : Mapped[str | None] = mapped_column(String, nullable=True)
    nonce_issued_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=func.now())
    hashed_password : Mapped[str | None] = mapped_column(String, nullable=True)
    wallet_type : Mapped[WalletType] = mapped_column(Enum(WalletType, values_callable=lambda x: [e.value for e in x],  name="wallet_type_enum", create_type=True), nullable=False, default=WalletType.CUSTODIAL.value)
