from fastapi import Depends

from CORE.interfaces_repository.IwineRepository import IwineRepository
from CORE.interfaces_services.IwineService import IwineService
from ENTITIES.dto.DTO_wine_note import DTO_wine_note
from INFRASTRUCTURE.REPOSITORIES.wineRepository import wineRepository
from CORE.interfaces_repository.IregionRepository import IregionRepository
from INFRASTRUCTURE.REPOSITORIES.regionRepository import regionRepository


class wineService(IwineService):
    def __init__(self, wnrepo:IwineRepository=Depends(wineRepository),
                reg_repo:IregionRepository=Depends(regionRepository)):
      self.wine_repository = wnrepo
      self.region_repository = reg_repo
      
    async def saveNote(self,note:DTO_wine_note): 
        return await self.wine_repository.saveNote(note) 
      
    async def getWineList(self,filter:str):
      
      regions = await self.region_repository.getRegions()
      
      winelist = await self.wine_repository.getWineList(filter)
      
      for item in winelist:
       reg = next((reg for reg in regions if reg.regions_id == item.regions_id), None)
       item.region =reg
      
      
      return winelist
