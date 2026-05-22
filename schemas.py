from pydantic import BaseModel, Field

class AutorBaseModel(BaseModel):
    nombre: str
    nacionalidad: str

class LibroBaseModel(BaseModel):
    titulo: str
    autor: AutorBaseModel
    publicacion: str

class UsuarioBaseModel(BaseModel):
    nombre: str
    matricula: str
    contrasena: str
