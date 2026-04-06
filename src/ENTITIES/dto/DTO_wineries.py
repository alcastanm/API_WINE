from typing import Optional

from pydantic import BaseModel


class DTO_wineries(BaseModel):
    wineries_id :Optional[int]=None
    regions_id :Optional[int]=None
    winery_name :Optional[str]=None
    latitude :Optional[float]=None
    longitude :Optional[float]=None
    
    class Config:
        from_attributes=True