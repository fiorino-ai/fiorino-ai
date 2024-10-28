from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    realm_id = Column(String(24), ForeignKey('realms.id'), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    masked = Column(String(48), nullable=False)
    is_disabled = Column(Boolean, nullable=False, default=False)
    disabled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="api_keys")
    realm = relationship("Realm", back_populates="api_keys")
    usages = relationship("Usage", back_populates="api_key")
