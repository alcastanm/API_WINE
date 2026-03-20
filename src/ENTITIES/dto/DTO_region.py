from typing import Optional

from pydantic import BaseModel

class DTO_region(BaseModel):
    
    regions_id:Optional[int]=None
    name : Optional[str]=None
    country :Optional[str]=None
    description :Optional[str]=None
    active :Optional[bool]=None
    
    class Config:
        from_attributes=True