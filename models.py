from typing import Optional, Union
from pydantic import BaseModel

class Test(BaseModel):
    id: Optional[int]
    Age : Optional[int]
    Sexe : Optional[str]
    Ville : Optional[str]
