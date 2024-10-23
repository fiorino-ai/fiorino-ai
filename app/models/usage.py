from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    realm_id = Column(String(24), ForeignKey('realms.id'), nullable=False)
    llm_cost_id = Column(Integer, ForeignKey('llm_costs.id'), nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    total_model_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

    llm_cost = relationship("LLMCost")
    realm = relationship("Realm", back_populates="usages")
