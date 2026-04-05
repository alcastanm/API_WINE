from fastapi import APIRouter, Depends
from src.CONTROLLER.RESPONSES.customResponse import customResponse
from CORE.SERVICES.regionService import regionService
from CORE.interfaces_services.IregionService import IregionService


regionRoute = APIRouter()


@regionRoute.get("/regions")
async def getRegions(region_service:IregionService=Depends(regionService)):
    try:
      result = await region_service.getRegions()
      return customResponse(data=result,isSuccess=True,returnedMessage="well Done!!!")
    except Exception as e:
      return customResponse(data=None,isSuccess=False,returnedMessage=str(e))