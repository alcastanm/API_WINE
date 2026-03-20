from abc import ABC,abstractmethod
from ENTITIES.dto.DTO_wine_note import DTO_wine_note

class IwineService(ABC):
    
    @abstractmethod
    async def saveNote(self,note:DTO_wine_note):
        pass
    
    @abstractmethod
    async def getWineList(self,filter:str):
        pass