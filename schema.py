from pydantic import BaseModel, ConfigDict, EmailStr

# Schema base para receber dados (tem senha)
class BaseUsuario(BaseModel):
    username: str
    email: str  # Se tiver validator instalado, pode usar EmailStr
    password: str

# Schema público para devolver dados (SEM senha)
class UsuarioPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)
    
# Schema genérico de Usuário (caso precise no futuro)
class Usuario(BaseUsuario):
    id: int
    model_config = ConfigDict(from_attributes=True)