from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.ENTITIES.dto.DTO_region import DTO_region


class DTO_wine_note(BaseModel):
    
    wine_note_id : Optional[int] = None 
    wine_name  : Optional[str] = None 
    wine_type : Optional[str] = None 
    photo : Optional[str] = None 
    color_rating : Optional[int] = None 
    aroma_rating : Optional[int] = None 
    cuerpo_rating : Optional[int] = None 
    sabor_rating : Optional[int] = None 
    final_rating: Optional[int] = None 
    notes : Optional[str] = None 
    created_at :  Optional[datetime] = None
    email : Optional[str] = None 
    regions_id: Optional[int] = None 
    region:Optional[DTO_region]=None
    
    class Config:
        from_attributes=True
        