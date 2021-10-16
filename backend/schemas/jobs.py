from typing import Optional
from typing_extensions import runtime
from pydantic import BaseModel
from datetime import date,datetime

class JobBase(BaseModel):
    title : Optional[str] = None
    company : Optional[str] = None
    company_url : Optional[str]  = None
    location : Optional[str] ="Remote"
    descriptions : Optional[str] = None
    data_posted : date = datetime.now().date()


class JobCreate(JobBase):
    title : str 
    company : str 
    location : str
    descriptions : str



class ShowJob(JobBase):
    title : str
    company : str
    company_url : Optional[str]
    location : str
    data_posted : date
    descriptions : Optional[str]
    
    class Config:
        orm_mode = True 

