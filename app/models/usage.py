from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    realm_id = Column(String(24), ForeignKey('realms.id'), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id', ondelete='SET NULL'), nullable=True)
    llm_cost_id = Column(Integer, ForeignKey('llm_costs.id'), nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    total_model_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

    llm_cost = relationship("LLMCost")
    realm = relationship("Realm", back_populates="usages")
    api_key = relationship("APIKey", back_populates="usages")
    account = relationship("Account", back_populates="usages")
