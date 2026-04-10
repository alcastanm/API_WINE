from sqlalchemy import BOOLEAN, TEXT, VARCHAR, Column, Integer,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class regions(Base):
    __tablename__="regions"
    
    regions_id=Column(Integer,primary_key=True,nullable=False)
    name =Column(VARCHAR(100),nullable=False)
    country =Column(VARCHAR(100),nullable=False)
    description =Column(TEXT,nullable=False)
    active =Column(BOOLEAN,nullable=False) 
    mapeable=Column(BOOLEAN,nullable=False)   
    geojson = Column(VARCHAR(500),nullable=False)
    url = Column(VARCHAR(1000),nullable=True)
    lat = Column(Float,nullable=True)
    long = Column(Float,nullable=True)
    climate = Column(Float,nullable=True)
    altitude = Column(Float,nullable=True)