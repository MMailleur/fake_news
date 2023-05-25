from typing import Optional, Union
from pydantic import BaseModel

class Test(BaseModel):
    id: Optional[int]
    title : Optional[str]
    author : Optional[str]
    text : Optional[str]
    label : Optional[int]

class Model_out(BaseModel):
    id: Optional[int]
    title : Optional[str]
    author : Optional[str]
    text : Optional[str]
    label : Optional[int]
