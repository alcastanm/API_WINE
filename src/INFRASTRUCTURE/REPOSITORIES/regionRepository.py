from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from CORE.interfaces_repository.IregionRepository import IregionRepository
from ENTITIES.domine.regions import regions
from ENTITIES.dto.DTO_region import DTO_region
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db

class regionRepository(IregionRepository):
    def __init__(self, db:AsyncSession=Depends(get_db)):
      self.dbconn = db
      
    async def getRegions(self):
        query = select(regions) 
        
        results = (await self.dbconn.execute(query)).scalars().all()
        
        return [DTO_region.model_validate(r) for r in results] if results else None
