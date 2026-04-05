from fastapi import Depends

from CORE.interfaces_repository.IregionRepository import IregionRepository
from CORE.interfaces_services.IregionService import IregionService
from INFRASTRUCTURE.REPOSITORIES.regionRepository import regionRepository


class regionService(IregionService):
    
    def __init__(self, regRepo:IregionRepository=Depends(regionRepository)):
      self.region_repository = regRepo

    async def getRegions(self):
        return await self.region_repository.getRegions()
        