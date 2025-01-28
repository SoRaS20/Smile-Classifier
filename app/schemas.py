from pydantic import BaseModel
from datetime import datetime

class HistoryBase(BaseModel):
    image_path: str
    result: str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  
