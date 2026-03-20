from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import Base
from datetime import datetime, timezone



class UsersModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    name = Column(String(150))
    picture = Column(String)
    provider = Column(String(50))
    created_at = Column(DateTime(timezone=True),nullable=True,default=datetime.now(timezone.utc))