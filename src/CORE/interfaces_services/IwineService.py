from abc import ABC,abstractmethod
from ENTITIES.dto.DTO_wine_note import DTO_wine_note

class IwineService(ABC):
    
    @abstractmethod
    async def saveNote(self,note:DTO_wine_note):
        pass
    
    @abstractmethod
    async def updateNote(self,note:DTO_wine_note):
        pass
    
    @abstractmethod
    async def getWineList(self,filter:str,mail:str):
        pass
    
    @abstractmethod
    async def getNote(self,noteid:int):
        pass