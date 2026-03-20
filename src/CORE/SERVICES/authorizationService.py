from fastapi import Depends

from CORE.interfaces_repository.IauthorizationRepository import IauthorizationRepository
from CORE.interfaces_services.IauthorizationService import IauthorizationService
from ENTITIES.domine.UsersModel import UsersModel
from INFRASTRUCTURE.REPOSITORIES.authorizationRepository import authorizationRepository


class authorizationService(IauthorizationService):
    
    def __init__(self, authRepo:IauthorizationRepository=Depends(authorizationRepository)):
      self.authorization_repository = authRepo

    
    async def saveUser(self,user:UsersModel):
        return await self.authorization_repository.saveUser(user)