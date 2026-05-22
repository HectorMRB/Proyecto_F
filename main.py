from fastapi import FastAPI
from database import database as connection
from database import Autor, Libro, Usuario, Prestamo
from schemas import AutorBaseModel, LibroBaseModel, UsuarioBaseModel

app = FastAPI(
    title="Biblioteca",
    description="Pproyecto final",
    version="1.0",
)



@app.on_event("startup")
async def startup():
    print("El servidor esta iniciando")
    if connection.is_closed():
        connection.connect()
        print('se inicio la conexion con la base de datos')


    connection.create_tables([Autor, Libro, Usuario, Prestamo])



@app.on_event("shutdown")
async def shutdown():
    print("El servidor esta finalizando")
    if not connection.is_closed():
        connection.close()
        print('se finalizo la conexion con la base de datos')



@app.get("/")
async def index():
    return "Biblioteca"

@app.post('/autores/')
async def create_autors(autor: AutorBaseModel):
    autor_creado = Autor.create(
        nombre=autor.nombre,
        ncionalidad=autor.nacionalidad
    )
    return {"id": autor_creado.id, "mensaje": "Autor registrado"}

@app.post('/libros/')
async def create_libros(libro: LibroBaseModel):
    libro_creado = Libro.create(
        titulo=libro.titulo,
        autor=libro.autor,
        publicacion=libro.publicacion
    )
    return {"id": libro_creado.id, "mensaje": "Libro registrado"}

@app.post('/usuarios/')
async def create_usuario(usuario: UsuarioBaseModel):
    usuario_creado = Usuario.create(
        nombre=usuario.nombre,
        matricula=usuario.matricula,
        contrasena=usuario.contrasena
    )
    return {"id": usuario_creado.id, "mensaje": "Usuario registrado"}