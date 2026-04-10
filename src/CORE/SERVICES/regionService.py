from fastapi import Depends

from CORE.interfaces_repository.IregionRepository import IregionRepository
from CORE.interfaces_repository.IwineriesRepository import IwineriesRepository
from CORE.interfaces_services.IregionService import IregionService
from INFRASTRUCTURE.REPOSITORIES.regionRepository import regionRepository
from INFRASTRUCTURE.REPOSITORIES.wineriesRepository import wineriesRepository


class regionService(IregionService):
    
    def __init__(self, regRepo:IregionRepository=Depends(regionRepository),
                       wineriesRepo:IwineriesRepository=Depends(wineriesRepository)):
      self.region_repository = regRepo
      self.wineries_rpository= wineriesRepo

    async def getRegions(self):
        regions = await self.region_repository.getRegions()
        
        for item in regions:
          wineries = await self.wineries_rpository.getWinneriesByRegionId(item.regions_id)
          item.wineries = wineries
          
          
        
        return regions 
        