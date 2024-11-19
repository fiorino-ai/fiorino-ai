from sqlalchemy import Column, Float, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Overhead(Base):
    __tablename__ = "overheads"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    realm_id = Column(String(24), ForeignKey('realms.id', ondelete='CASCADE'), nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))
    percentage = Column(Float, nullable=False)

    realm = relationship("Realm", back_populates="overheads")
