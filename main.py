from fastapi import FastAPI
from database import database as connection
from database import Autor, Libro, Usuario, Prestamo
from schemas import AutorBaseModel, LibroBaseModel, UsuarioBaseModel, LibroUpdateModel, PrestamoBaseModel, PrestamoUpdateModel
from peewee import fn
#Por depreciacición: "on_event is deprecated, use lifespan event handlers instead."
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("El servidor esta iniciando")
    if connection.is_closed():
        connection.connect()
        print('se inicio la conexion con la base de datos')

    connection.create_tables([Autor, Libro, Usuario, Prestamo])
    #Yiel separa el incio del final del servidor
    yield
    print("El servidor esta finalizando")
    if not connection.is_closed():
        connection.close()
        print('se finalizo la conexion con la base de datos')

app = FastAPI(
    lifespan=lifespan,
    title="Biblioteca",
    description="Pproyecto final",
    version="2.0",
)

@app.get("/")
async def index():
    return "Biblioteca"

@app.post('/autores/')
async def create_autors(autor: AutorBaseModel):
    autor_creado = Autor.create(
        nombre=autor.nombre,
        nacionalidad=autor.nacionalidad
    )
    return {"id": autor_creado.id, "mensaje": "Autor registrado"}

@app.post('/usuarios/')
async def create_usuario(usuario: UsuarioBaseModel):
    usuario_creado = Usuario.create(
        nombre=usuario.nombre,
        matricula=usuario.matricula,
        contrasena=usuario.contrasena
    )
    return {"id": usuario_creado.id, "mensaje": "Usuario registrado"}

@app.post('/libros/')
async def create_libros(libro: LibroBaseModel):
    libro_creado = Libro.create(
        titulo=libro.titulo,
        autor=libro.autor_id,
        publicacion=libro.publicacion
    )
    return {"id": libro_creado.id, "mensaje": "Libro registrado"}

@app.post('/prestamos/')
async def create_prestamo(prestamo: PrestamoBaseModel):
    prestamo_creado = Prestamo.create(
        libro_id=prestamo.libro_id,
        usuario_id=prestamo.usuario_id,
    )
    return {"id:": prestamo_creado.id, "mensaje": "Prestamo registrado"}

@app.get('/autoresL/')
async def get_autors():
    autores = Autor.select()
    resultado = []
    for autor in autores:
        resultado.append({
            "id": autor.id,
            "nombre": autor.nombre,
            "nacionalidad": autor.nacionalidad
        })
    return resultado

@app.get('/librosL/')
async def get_libros():
    libros = Libro.select()
    resultado = []
    for libro in libros:
        resultado.append({
            "id": libro.id,
            "titulo": libro.titulo,
            "autor_id": libro.autor.id,
            "publicacion": libro.publicacion
        })
    return resultado

@app.get('/libros/top')
async def libros_populares():
    res = Prestamo.select(Prestamo.libro_id, fn.COUNT(Prestamo.id).alias('total')).group_by(Prestamo.libro_id)
    return [{"libro_id": x.libro_id, "cantidad_prestamos": x.total} for x in res]

@app.get('/usuariosL/')
async def get_usuario():
    usuario_creado = Usuario.select()
    resultado = []
    for usuario in usuario_creado:
        resultado.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "matricula": usuario.matricula,
            "contrasena": usuario.contrasena
        })
    return resultado

@app.get('/prestamosL/')
async def get_prestamos():
    prestamos = Prestamo.select()
    resultado = []
    for prestamo in prestamos:
        resultado.append({
            "id": prestamo.id,
            "libro_id": prestamo.libro.id,
            "usuario_id": prestamo.usuario.id,
            "fecha_p": prestamo.fecha_p,
            "fecha_d": prestamo.fecha_d,
        })
    return resultado

@app.put('/libros/{libro_id}')
async def update_libro(libro_id: int, datos: LibroUpdateModel):
    libro = Libro.get(Libro.id == libro_id)
    if datos.titulo is not None:
        libro.titulo = datos.titulo
    if datos.autor_id is not None:
        libro.autor_id = datos.autor_id
    if datos.publicacion is not None:
        libro.publicacion = datos.publicacion
    libro.save()

    return {"id": libro_id, "mensaje": "Libro actualizado"}

@app.put('/prestamos/{prestamo_id}')
async def update_prestamo(prestamo_id: int, datos: PrestamoUpdateModel):
    prestamo = Prestamo.get(Prestamo.id == prestamo_id)
    prestamo.fecha_d = datos.fecha_d
    prestamo.save()
    return {"mensaje": "Libro devuelto, fecha registrada"}