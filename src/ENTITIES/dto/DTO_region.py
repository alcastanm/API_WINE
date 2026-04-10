from typing import Optional
from pydantic import BaseModel
from ENTITIES.dto.DTO_wineries import DTO_wineries

class DTO_region(BaseModel):
    
    regions_id:Optional[int]=None
    name : Optional[str]=None
    country :Optional[str]=None
    description :Optional[str]=None
    active :Optional[bool]=None
    mapeable:Optional[bool]=None
    geojson:Optional[str]=None
    wineries:Optional[list[DTO_wineries]]=None   
    url:Optional[str]=None
    lat:Optional[float]=None
    long:Optional[float]=None
    climate:Optional[float]=None
    altitude:Optional[float]=None
    class Config:
        from_attributes=True