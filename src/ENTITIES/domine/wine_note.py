from sqlalchemy import TEXT, VARCHAR, Column, Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base =declarative_base()

class wine_note(Base):
    __tablename__="wine_notes"
    
    wine_note_id = Column(Integer,primary_key=True)
    wine_name  = Column(VARCHAR(50),nullable=True)  
    wine_type = Column(VARCHAR(50),nullable=False) 
    photo = Column(VARCHAR(1000),nullable=False) 
    color_rating = Column(Integer,nullable=False) 
    aroma_rating = Column(Integer,nullable=False) 
    cuerpo_rating = Column(Integer,nullable=False) 
    sabor_rating = Column(Integer,nullable=False) 
    final_rating= Column(Integer,nullable=False) 
    notes = Column(TEXT,nullable=False) 
    created_at = Column(DateTime(timezone=True),nullable=True,default=datetime.now(timezone.utc))  
    email = Column(VARCHAR(150),nullable=False) 
    regions_id = Column(Integer,nullable=False)