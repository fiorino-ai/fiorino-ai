from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy import UniqueConstraint

class LLMCost(Base):
  __tablename__ = "llm_costs"

  id = Column(Integer, primary_key=True, index=True)
  provider_name = Column(String, nullable=False)
  model_name = Column(String, nullable=False)
  price_per_unit = Column(Float, nullable=False)
  unit_type = Column(String(20), nullable=False)
  overhead_percentage = Column(Float, default=0)
  valid_from = Column(DateTime, nullable=False)
  valid_to = Column(DateTime)
  is_system = Column(Boolean, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  

  __table_args__ = (
    UniqueConstraint('provider_name', 'model_name', 'valid_from', name='uix_provider_model_valid_from'),
  )
