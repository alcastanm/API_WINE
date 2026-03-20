from abc import ABC,abstractmethod

from ENTITIES.domine.UsersModel import UsersModel

class IauthorizationRepository(ABC):
    
    @abstractmethod
    async def saveUser(self,user:UsersModel):
        pass

