from pydantic import BaseModel
from models.data.sqlalchemy_data import UserType

class UserReq(BaseModel): 
    id : int 
    nombre: str 
    password: str 
    tipo: UserType
        
    class Config:
        orm_mode = True