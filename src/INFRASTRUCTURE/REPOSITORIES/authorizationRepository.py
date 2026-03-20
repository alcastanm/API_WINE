from fastapi import Depends
from sqlalchemy import select

from CORE.interfaces_repository.IauthorizationRepository import IauthorizationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ENTITIES.domine.UsersModel import UsersModel
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db


class authorizationRepository(IauthorizationRepository):
    def __init__(self, db:AsyncSession=Depends(get_db)):
      self.dbConn = db
      
    async def saveUser(self,user:UsersModel):   
        query = select(UsersModel).where(UsersModel.email==user.email).limit(1)
        result = (await self.dbConn.execute(query)).scalar_one_or_none()
        
        if(not result):
            user.id=None
            self.dbConn.add(user)
            self.dbConn.flush()
            result= user
            await self.dbConn.commit()
            await self.dbConn.refresh(user)
        else:
            user.id = result.id
            result= user
            
        return  result
