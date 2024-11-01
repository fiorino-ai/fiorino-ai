from sqlalchemy import Column, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

class LLMCost(Base):
    __tablename__ = "llm_costs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    llm_id = Column(UUID(as_uuid=True), ForeignKey('large_language_models.id', ondelete='CASCADE'), nullable=False)
    realm_id = Column(String(24), ForeignKey('realms.id', ondelete='CASCADE'), nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit_type = Column(String(20), nullable=False)
    overhead = Column(Float, default=0)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    llm = relationship("LargeLanguageModel")
    realm = relationship("Realm", back_populates="llm_costs")
    usages = relationship("Usage", back_populates="llm_cost", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('llm_id', 'valid_from', name='uix_llm_valid_from'),
    )
