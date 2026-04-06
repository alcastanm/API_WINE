from sqlalchemy import NUMERIC, VARCHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class wineries(Base):
    __tablename__ = "wineries"
    
    wineries_id = Column(Integer,primary_key=True,nullable=False)
    regions_id = Column(Integer,nullable=False)
    winery_name = Column(VARCHAR(200),nullable=False)
    latitude = Column(NUMERIC(9, 6),nullable=False)
    longitude = Column(NUMERIC(9, 6),nullable=False) 