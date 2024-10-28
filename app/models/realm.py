from sqlalchemy import Column, String, DateTime, ForeignKey, text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class Realm(Base):
    __tablename__ = "realms"

    id = Column(String(24), primary_key=True, server_default=text("generate_object_id()"), index=True)
    name = Column(String(255), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    bill_limit_enabled = Column(Boolean, nullable=False, default=False)
    overhead_enabled = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="realms")
    api_keys = relationship("APIKey", back_populates="realm")
    usages = relationship("Usage", back_populates="realm")
    bill_limits = relationship("BillLimit", back_populates="realm", cascade="all, delete-orphan")
    overheads = relationship("Overhead", back_populates="realm", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="realm", cascade="all, delete-orphan")
