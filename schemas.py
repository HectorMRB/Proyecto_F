from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class AutorBaseModel(BaseModel):
    nombre: str
    nacionalidad: str

    @field_validator('nombre','nacionalidad')
    def validar_longitud(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('La longitud debe contener minimo 3 caracteres y hasta 50 caracteres')
        return value.strip()

class LibroBaseModel(BaseModel):
    titulo: str
    autor_id: int
    publicacion: int

    @field_validator('titulo')
    def titulo_validar(cls, value):
        if len(value) < 3 or len(value) > 100:
            raise ValueError('La longitud debe contener minimo 3 caracteres y hasta 100 caracteres')
        
    @field_validator('publicacion')
    def publicacion_validar(cls, value):
        anio = datetime.now().year

        if value < 1000 or value > anio:
            raise ValueError(f"El año de publicacion debe ser valido entre 1000 y {anio}")
        return value

class LibroUpdateModel(BaseModel):
    titulo: Optional[str] = None
    autor_id: Optional[int] = None
    publicacion: Optional[int] = None

    @field_validator('titulo')
    def titulo_validar(cls, value):
        if len(value) < 5 or len(value) > 500:
            raise ValueError('La longitud debe contener minimo 5 caracteres y hasta 500 caracteres')
        return value

class UsuarioBaseModel(BaseModel):
    nombre: str
    matricula: str
    contrasena: str

    @field_validator('nombre')
    def nombre_validar(cls, value):
        if len(value) < 5 or len(value) > 50:
            raise ValueError('La longitud debe contener minimo 5 caracteres y hasta 50 caracteres')
        return value.strip()

class PrestamoBaseModel(BaseModel):
    libro_id: int
    usuario_id: int

class PrestamoUpdateModel(BaseModel):
    fecha_d: str