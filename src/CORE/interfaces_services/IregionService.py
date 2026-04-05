from abc import ABC,abstractmethod

class IregionService(ABC):
    
    @abstractmethod
    async def getRegions(self):
        pass