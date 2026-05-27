from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import httpx
import uvicorn

app = FastAPI(title="Cliente")

url = "http://127.0.0.1:8000"

def generar_html(contenido):
    html = f"""
    <html>
    <head>
        <title>Biblioteca</title>
    </head>
    <body bgcolor="#ffffff" text="#000000">
        <h1>Sistema de biblioteca</h1>
        <hr>
        <a href="/autores_web">Autores</a>
        <a href="/libros_web">Libros</a>
        <a href="/usuarios_web">Usuarios</a>
        <a href="/prestamos_web">Prestamos</a>
        <hr>
        <br>
        {contenido}
    </body>
    </html>
    """
    return html

@app.get("/", response_class=HTMLResponse)
@app.get("/autores_web", response_class=HTMLResponse)
async def ver_autores():
    async with httpx.AsyncClient() as client:
        respuesta = await client.get(f"{url}/autoresL/")
        autores = respuesta.json() if respuesta.status_code == 200 else []

    tabla = "<table border='1'><tr><th>ID</th><th>Nombre</th><th>Nacionalidad</th></tr>"
    for a in autores:
        tabla += f"<tr><td>{a['id']}</td><td>{a['nombre']}</td><td>{a['nacionalidad']}</td></tr>"
    tabla += "</table>"

    boton = "<br><a href='/agregar_autores_web'>Registrar autor</a><br><br>"
    return generar_html("<h2>Lista de autores</h2>" + boton + tabla)

@app.get("/agregar_autores_web", response_class=HTMLResponse)
async def form_agregar_autores():
    formulario = """
    <h2>Registrar nuevo autor</h2>
    <form action="/agregar_autores_web" method="post">
        Nombre: <input type="text" name="nombre" required><br><br>
        Nacionalidad: <input type="text" name="nacionalidad" required><br><br>
        <input type="submit" value="Guardar Autor">
    </form>
    <br><a href='/autores_web'>Volver</a>
    """
    return generar_html(formulario)

@app.post("/agregar_autores_web", response_class=HTMLResponse)
async def guardar_autor(nombre: str = Form(...), nacionalidad: str = Form(...)):
    async with httpx.AsyncClient() as client:
        respuesta = await client.post(f"{url}/autores/", json={"nombre": nombre, "nacionalidad": nacionalidad})
        
    if respuesta.status_code == 200:
        return generar_html("<b>Autor registrado con exito</b><br><br><a href='/autores_web'>Regresar</a>")
    else:
        return generar_html(f"<h3>Error al registrar</h3><p>{respuesta.text}</p><a href='/agregar_autores_web'>Intentar de nuevo</a>")

@app.get("/libros_web", response_class=HTMLResponse)
async def ver_libros():
    async with httpx.AsyncClient() as client:
        respuesta = await client.get(f"{url}/librosL/")
        libros = respuesta.json() if respuesta.status_code == 200 else []

    tabla = "<table border='1'><tr><th>ID</th><th>Titulo</th><th>ID autor</th><th>Publicacion</th></tr>"
    for lib in libros:
        tabla += f"<tr><td>{lib['id']}</td><td>{lib['titulo']}</td><td>{lib['autor_id']}</td><td>{lib['publicacion']}</td></tr>"
    tabla += "</table>"

    boton = "<br><a href='/agregar_libros_web'>Registrar libro</a><br><br>"
    return generar_html("<h2>Lista de libros</h2>" + boton + tabla)

@app.get("/agregar_libros_web", response_class=HTMLResponse)
async def form_agregar_libros():
    formulario = """
    <h2>Registrar libro</h2>
    <form action="/agregar_libros_web" method="post">
        Titulo: <input type="text" name="titulo" required><br><br>
        ID del autor: <input type="number" name="autor_id" required><br><br>
        Año de publicacion: <input type="number" name="publicacion" required><br><br>
        <input type="submit" value="Guardar libro">
    </form>
    <br><a href='/libros_web'>Volver</a>
    """
    return generar_html(formulario)

@app.post("/agregar_libros_web", response_class=HTMLResponse)
async def guardar_libro(titulo: str = Form(...), autor_id: int = Form(...), publicacion: int = Form(...)):
    async with httpx.AsyncClient() as client:
        respuesta = await client.post(f"{url}/libros/", json={"titulo": titulo, "autor_id": autor_id, "publicacion": publicacion})
        
    if respuesta.status_code == 200:
        return generar_html("<b>Libro guardado con exito</b><br><br><a href='/libros_web'>Regresar</a>")
    else:
        return generar_html(f"<h3>Error al registrar</h3><p>{respuesta.text}</p><a href='/agregar_libros_web'>Intentar de nuevo</a>")

@app.get("/usuarios_web", response_class=HTMLResponse)
async def ver_usuarios():
    async with httpx.AsyncClient() as client:
        respuesta = await client.get(f"{url}/usuariosL/")
        usuarios = respuesta.json() if respuesta.status_code == 200 else []

    tabla = "<table border='1'><tr><th>ID</th><th>Nombre</th><th>Matricula</th></tr>"
    for u in usuarios:
        tabla += f"<tr><td>{u['id']}</td><td>{u['nombre']}</td><td>{u['matricula']}</td></tr>"
    tabla += "</table>"

    boton = "<br><a href='/agregar_usuarios_web'>Registrar usuario</a><br><br>"
    return generar_html("<h2>Lista de usuarios</h2>" + boton + tabla)

@app.get("/agregar_usuarios_web", response_class=HTMLResponse)
async def form_agregar_usuarios():
    formulario = """
    <h2>Registrar usuario</h2>
    <form action="/agregar_usuarios_web" method="post">
        Nombre: <input type="text" name="nombre" required><br><br>
        Matricula: <input type="text" name="matricula" required><br><br>
        Contraseña: <input type="password" name="contrasena" required><br><br>
        <input type="submit" value="Guardar usuario">
    </form>
    <br><a href='/usuarios_web'>Volver</a>
    """
    return generar_html(formulario)

@app.post("/agregar_usuarios_web", response_class=HTMLResponse)
async def guardar_usuario(nombre: str = Form(...), matricula: str = Form(...), contrasena: str = Form(...)):
    async with httpx.AsyncClient() as client:
        respuesta = await client.post(f"{url}/usuarios/", json={"nombre": nombre, "matricula": matricula, "contrasena": contrasena})
        
    if respuesta.status_code == 200:
        return generar_html("<b>Usuario registrado</b><br><br><a href='/usuarios_web'>Regresar</a>")
    else:
        return generar_html(f"<h3>Error al registrar</h3><p>{respuesta.text}</p><a href='/agregar_usuarios_web'>Intentar de nuevo</a>")

@app.get("/prestamos_web", response_class=HTMLResponse)
async def ver_prestamos():
    async with httpx.AsyncClient() as client:
        respuesta = await client.get(f"{url}/prestamosL/")
        prestamos = respuesta.json() if respuesta.status_code == 200 else []

    tabla = "<table border='1'><tr><th>ID</th><th>Libro ID</th><th>Usuario ID</th><th>Fecha prestamo</th><th>Fecha devolucion</th></tr>"
    for p in prestamos:
        fecha_d = p['fecha_d'] if p['fecha_d'] else "PENDIENTE"
        tabla += f"<tr><td>{p['id']}</td><td>{p['libro_id']}</td><td>{p['usuario_id']}</td><td>{p['fecha_p']}</td><td>{fecha_d}</td></tr>"
    tabla += "</table>"

    botones = """
    <br>
    <a href='/agregar_prestamos_web'>Nuevo prestamo</a>
    <a href='/editar_prestamos_web'>Registrar devolucion</a><br><br>
    """
    return generar_html("<h2>Lista de prestamos</h2>" + botones + tabla)

@app.get("/agregar_prestamos_web", response_class=HTMLResponse)
async def form_agregar_prestamos():
    formulario = """
    <h2>Realizar Prestamo</h2>
    <form action="/agregar_prestamos_web" method="post">
        ID del libro: <input type="number" name="libro_id" required><br><br>
        ID del usuario: <input type="number" name="usuario_id" required><br><br>
        <input type="submit" value="Prestar Libro">
    </form>
    <br><a href='/prestamos_web'>Volver</a>
    """
    return generar_html(formulario)

@app.post("/agregar_prestamos_web", response_class=HTMLResponse)
async def crear_prestamo(libro_id: int = Form(...), usuario_id: int = Form(...)):
    async with httpx.AsyncClient() as client:
        respuesta = await client.post(f"{url}/prestamos/", json={"libro_id": libro_id, "usuario_id": usuario_id})
        
    if respuesta.status_code == 200:
        return generar_html("<b>Prestamo realizado</b><br><br><a href='/prestamos_web'>Regresar</a>")
    else:
        return generar_html(f"<h3>Error al registrar</h3><p>{respuesta.text}</p><a href='/agregar_prestamos_web'>Intentar de nuevo</a>")

@app.get("/editar_prestamos_web", response_class=HTMLResponse)
async def form_editar_prestamos():
    formulario = """
    <h2>Actualizar devolucion</h2>
    <form action="/editar_prestamos_web" method="post">
        ID del prestamo: <input type="number" name="prestamo_id" required><br><br>
        Fecha devolucion (yyyy-mm-dd): <input type="text" name="fecha_d" required><br><br>
        <input type="submit" value="Registrar devolucion">
    </form>
    <br><a href='/prestamos_web'>Volver</a>
    """
    return generar_html(formulario)

@app.post("/editar_prestamos_web", response_class=HTMLResponse)
async def devolver_prestamo(prestamo_id: int = Form(...), fecha_d: str = Form(...)):
    async with httpx.AsyncClient() as client:
        respuesta = await client.put(f"{url}/prestamos/{prestamo_id}", json={"fecha_d": fecha_d})
        
    if respuesta.status_code == 200:
        return generar_html("<b>Devolucion registrada</b><br><br><a href='/prestamos_web'>Regresar</a>")
    else:
        return generar_html(f"<h3>Error al actualizar</h3><p>{respuesta.text}</p><a href='/editar_prestamos_web'>Intentar de nuevo</a>")

if __name__ == "__main__":
    print("Iniciando el cliente")
    uvicorn.run(app, host="127.0.0.1", port=8001)