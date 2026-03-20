from sqlalchemy import BOOLEAN, TEXT, VARCHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class regions(Base):
    __tablename__="regions"
    
    regions_id=Column(Integer,primary_key=True,nullable=False)
    name =Column(VARCHAR(100),nullable=False)
    country =Column(VARCHAR(100),nullable=False)
    description =Column(TEXT,nullable=False)
    active =Column(BOOLEAN,nullable=False)    