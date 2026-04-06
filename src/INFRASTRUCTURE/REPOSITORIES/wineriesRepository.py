from fastapi import Depends
from sqlalchemy import select

from CORE.interfaces_repository.IwineriesRepository import IwineriesRepository
from ENTITIES.domine.wineries import wineries
from ENTITIES.dto.DTO_wineries import DTO_wineries
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession


class wineriesRepository(IwineriesRepository):
    
    def __init__(self, db:AsyncSession=Depends(get_db)):
      self.dbConn = db
    
    
    async def getWinneriesByRegionId(self,regionId:int):
        query = select(wineries).where(wineries.regions_id==regionId)
        results = (await self.dbConn.execute(query)).scalars().all()
        
        return [DTO_wineries.model_validate(r) for r in results] if results else None


