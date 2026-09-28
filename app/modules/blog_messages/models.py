# models go here
from ...db.database import Base
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped


class Blog(Base):
    __tablename__="blogs"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    writer_id: Mapped[int] = mapped_column(ForeignKey("writers.id"))
    writer:Mapped["Writer"] = relationship(back_populates="blogs")
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
