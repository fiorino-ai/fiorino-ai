from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class BillLimit(Base):
    __tablename__ = "bill_limits"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    realm_id = Column(String(24), ForeignKey('realms.id'), nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))
    amount = Column(Float, nullable=False)

    realm = relationship("Realm", back_populates="bill_limits")
