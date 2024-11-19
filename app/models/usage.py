from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    realm_id = Column(String(24), ForeignKey('realms.id', ondelete='CASCADE'), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id', ondelete='SET NULL'), nullable=True)
    llm_cost_id = Column(UUID(as_uuid=True), ForeignKey('llm_costs.id', ondelete='CASCADE'), nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    total_model_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    llm_cost = relationship("LLMCost", back_populates="usages")
    realm = relationship("Realm", back_populates="usages")
    api_key = relationship("APIKey", back_populates="usages")
    account = relationship("Account", back_populates="usages")
