from pydantic import BaseModel, ConfigDict, EmailStr

class BaseUsuario(BaseModel):
    username: str
    email: str  
    password: str


class UsuarioPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class Usuario(BaseUsuario):
    id: int
    model_config = ConfigDict(from_attributes=True)