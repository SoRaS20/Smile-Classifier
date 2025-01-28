from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class History(Base):
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)
    result = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
