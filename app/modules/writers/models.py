from ...db.database import Base
from sqlalchemy import DateTime, func, String
import uuid 
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Writer(Base):
    __tablename__ ="writers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    call_sign : Mapped[str] = mapped_column(String(50), nullable=False)
    signature: Mapped[str] = mapped_column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    blogs:Mapped[list["Blog"]] = relationship(back_populates="writer", cascade="all, delete-orphan")
