from abc import ABC,abstractmethod


class IregionRepository(ABC):
    
    @abstractmethod
    async def getRegions(self):
        pass