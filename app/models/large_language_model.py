from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class LargeLanguageModel(Base):
    __tablename__ = "large_language_models"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    realm_id = Column(String(24), ForeignKey('realms.id', ondelete='CASCADE'), nullable=False)
    provider_name = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    realm = relationship("Realm", back_populates="large_language_models")

    __table_args__ = (
        # Ensure unique combination of realm_id, provider_name, and model_name
        UniqueConstraint('realm_id', 'provider_name', 'model_name', name='uix_realm_provider_model'),
    ) 