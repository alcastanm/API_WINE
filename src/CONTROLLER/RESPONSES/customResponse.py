from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class customResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    isSuccess: bool = True
    returnedMessage:str=""  
    returnTechnicalMessage : str=""
            