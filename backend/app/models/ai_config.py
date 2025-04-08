from sqlalchemy import Boolean, Column, Integer, String, Float, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base

class StoreLevel(str, enum.Enum):
    STORE = "store"
    PRODUCT = "product"
    USER_ID = "user_id"

class AIConfig(Base):
    __tablename__ = "ai_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    store_level = Column(Enum(StoreLevel), default=StoreLevel.USER_ID)
    faq_threshold = Column(Float, default=0.75)  # Threshold for FAQ accuracy
    custom_prompt = Column(Text)  # Custom prompt for the AI agent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="ai_config")
