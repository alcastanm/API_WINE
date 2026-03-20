from fastapi import Depends
from sqlalchemy import insert, select

from CORE.interfaces_repository.IwineRepository import IwineRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ENTITIES.domine.wine_note import wine_note
from ENTITIES.dto.DTO_wine_note import DTO_wine_note
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db


class wineRepository(IwineRepository):
    def __init__(self, db:AsyncSession=Depends(get_db)):
      self.dbConn = db
      
    async def saveNote(self,note:DTO_wine_note):
        query = insert(wine_note).values(wine_name = note.wine_name,
                                        wine_type = note.wine_type,
                                        photo = note.photo,
                                        color_rating = note.color_rating,
                                        aroma_rating = note.aroma_rating,
                                        cuerpo_rating = note.cuerpo_rating,
                                        sabor_rating = note.sabor_rating,
                                        final_rating = note.final_rating,
                                        notes = note.notes,
                                        created_at = note.created_at,
                                        email = note.email,
                                        regions_id = note.regions_id)
        await self.dbConn.execute(query)
        await self.dbConn.commit()
        
        return True
      
    async def getWineList(self,filter:str):

      if filter == 'todos':
        query = select(wine_note)
      else:
        query = select(wine_note).where(wine_note.wine_type==filter)  
        
      result = (await self.dbConn.execute(query)).scalars().all()
      
            
      return [DTO_wine_note.model_validate(res) for res in result] if result else None     
