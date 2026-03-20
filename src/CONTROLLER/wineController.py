from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from CORE.SERVICES.wineService import wineService
from CORE.interfaces_services.IwineService import IwineService
from HELPERS.ImagesManagement import ImagesManagement
from src.ENTITIES.dto.DTO_wine_note import DTO_wine_note
from datetime import datetime, timezone
from CORE.SECURITY.auth_dependency import get_current_user
from src.CONTROLLER.RESPONSES.customResponse import customResponse


wineRoute = APIRouter()


@wineRoute.post("/wine")
async def saveNote( wine_name: str = Form(...),
                wine_type: str = Form(...),
                color_rating: Optional[int] = Form(0),
                aroma_rating: Optional[int] = Form(0),
                cuerpo_rating: Optional[int] = Form(0),
                sabor_rating: Optional[int] = Form(0),
                final_rating: Optional[int] = Form(0),
                notes: Optional[str] = Form(''),
                email:str =Form(...),
                photo: Optional[UploadFile] = File(None),
                regionId: int = Form(...),
                wine_service:IwineService=Depends(wineService)):
    try:
        
        

        
        currentDate = datetime.now(timezone.utc)
        note = DTO_wine_note(wine_name = wine_name,
                                wine_type = wine_type,
                                photo = photo.filename if photo else "",
                                color_rating = color_rating,
                                aroma_rating = aroma_rating,
                                cuerpo_rating = cuerpo_rating,
                                sabor_rating = sabor_rating,
                                final_rating = final_rating,
                                notes = notes,
                                created_at=currentDate,
                                email = email,
                                regions_id = regionId )
        
        result = await  wine_service.saveNote(note)
        
        if result == True:
            if photo:
                upldImg = await ImagesManagement.UploadImageCloudinary(photo,'wine')
        
        return customResponse(data=result,isSuccess=True,returnedMessage="La nota de cata se adicionó")
      
    except Exception as e:
      return customResponse(data=None,isSuccess=False,returnedMessage=str(e))
  

@wineRoute.get("/wines")  
async def getWineList(filter:str,wine_service:IwineService=Depends(wineService)):  
    try:
        result = await wine_service.getWineList(filter)
        return JSONResponse(
            content={
                "data": jsonable_encoder(result),
                "isSuccess": True,
                "returnedMessage": "Well Done",
                "returnTechnicalMessage": ""
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "data": None,
                "isSuccess": False,
                "returnedMessage": str(e),
                "returnTechnicalMessage": ""
            }
        )
    
