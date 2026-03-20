from typing import Optional

from pydantic import BaseModel

class googleParam(BaseModel):
    provider:Optional[str]=None
    token:Optional[str]=None