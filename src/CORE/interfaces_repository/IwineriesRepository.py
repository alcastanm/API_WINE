from abc import ABC,abstractmethod

class IwineriesRepository(ABC):
    
    @abstractmethod
    async def getWinneriesByRegionId(self,regionId:int):
        pass