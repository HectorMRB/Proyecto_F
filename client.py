from contextlib import asynccontextmanager
import asyncio
import httpx

url = "http://127.0.0.1:8000"

@asynccontextmanager
async def inicializar_cliente(url: str):
    async with httpx.AsyncClient(base_url=url) as cliente_activo:
        yield cliente_activo

async def infoUsuarios(cliente):
    respuesta = await cliente.get("/usuariosL/")
    print("\n==================== Mostrando lista de usuarios ====================")
    for usuario in respuesta.json():
        print(f"ID: {usuario.get('id')} - Nombre: {usuario.get('nombre')} - Matricula: {usuario.get('matricula')} - Contrasena: {usuario.get('contrasena')}")
    print("======================================================================\n")

async def infoLibros(cliente):
    respuesta = await cliente.get("/librosL/")
    print("\n============ Mostrando lista de libros ============")
    for libro in respuesta.json():
        print(f"ID: {libro.get('id')} - Titulo: {libro.get('titulo')} - Autor: {libro.get('autor_id')} - Publicacion: {libro.get('publicacion')}")
    print("==================================================\n")

async def infoPrestamos(cliente):
    respuesta = await cliente.get("/prestamosL/")
    print("\n======================================== Mostrando lista de prestamos ========================================")
    for prestamo in respuesta.json():
        print(f"ID: {prestamo.get('id')} - Libro: {prestamo.get('libro_id')} - Usuario: {prestamo.get('usuario_id')} - Fecha prestamo: {prestamo.get('fecha_p')} - Fecha devolucion: {prestamo.get('fecha_d')}")
    print("=============================================================================================================\n")

async def infoAutor(cliente):
    respuesta = await cliente.get("/autoresL/")
    print("\n============ Mostradno lista de autores ============")
    for autor in respuesta.json():
        print(f"ID: {autor.get('id')} - Nombre: {autor.get('nombre')} - nacionalidad: {autor.get('nacionalidad')}")
    print("==================================================\n")

async def infoTopLibros(cliente):
    respuesta = await cliente.get("/libros/top")
    print("\n==================================== TOP LIBROS MÁS PRESTADOS ====================================")
    for item in respuesta.json():
        print(f"ID Libro: {item.get('libro_id')} - Cantidad de Préstamos: {item.get('cantidad_prestamos')}")
    print("===================================================================================================\n")

async def main():
    print("\n==== Bienvenido al sistema de la biblioteca central ====")
    eleccion = 0

    async with inicializar_cliente(url) as cliente:
        while eleccion != 11:
            print("\n====== MENU ======")
            print("1) Registrar libros")
            print("2) Consultar libros")
            print("3) Actualizar libros")
            print("4) Resitrar usuarios")
            print("5) Consultar usuarios")
            print("6) resitrar préstamos")
            print("7) Actualizar devolucion préstamos")
            print("8) Consultar préstamos")
            print("9) Registar autores")
            print("10) Ver TOP libros más prestados")

            eleccion = int(input("Digite su opcion: "))

            match eleccion:
                case 1:
                    print("\nSeleccionó 'Registrar libros'")
                    nombre = input("Escriba el nombre: ")

                    await infoAutor(cliente)
                    try:
                        autor = int(input("Escriba el ID del autor: "))
                        publicacion = int(input("Escriba el año de publicacion: "))
                    except ValueError:
                        print("\nno se encontro id")
                        continue
                    respuesta = await cliente.post("/libros/", json={"titulo": nombre, "autor_id": autor, "publicacion": publicacion})

                    print(respuesta.json())
                case 2:
                    print("\nSeleccionó 'Consultar libros'")
                    await infoLibros(cliente)

                case 3:
                    print("\nSeleccionó 'Actualizar libros'")
                    await infoLibros(cliente)
                    libro_id = int(input("Escriba el ID del libro a actualizar: "))
                    titulo = input("Escriba el titulo del libro a actualizar: ")

                    autores = await cliente.get("/autoresL/")
                    print("===== Mostrando lista de autores =====")
                    print(f"{autores.json()}\n")

                    autor_input = input("Escriba el id del autor del libro a actualizar: ")
                    publicacion_input = input("Escriba la publicacion del libro a actualizar: ")

                    datos = {}
                    if titulo: datos["titulo"] = titulo
                    if autor_input: datos["autor_id"] = int(autor_input)
                    if publicacion_input: datos["publicacion"] = int(publicacion_input)

                    respuesta = await cliente.put(f"/libros/{libro_id}", json=datos)
                    print(respuesta.json())

                case 4:
                    print("\nSelecciono 'Registrar usuarios'")
                    nombre = input("Escriba el nombre del usuario: ")
                    matricula = input("Escriba la matricula 9 digitos: ")
                    while len(matricula) != 9 or not matricula.isdigit():
                        matricula = input("9 digitos: ")
                    contrasena = input("Contraseña: ")

                    respuesta = await cliente.post("/usuarios/", json={"nombre": nombre, "matricula": matricula, "contrasena": contrasena})
                    print(respuesta.json())
                case 5:
                    print("\nSeleccionó 'Consultar usuarios'")
                    await infoUsuarios(cliente)

                case 6:
                    print("\nSeleccionó 'registrar préstamos'")
                    await infoLibros(cliente)
                    libro_id = int(input("Escriba el ID del libro a registrar: "))
                    await infoUsuarios(cliente)
                    usuario_id = int(input("Escriba el ID del usuario a registrar: "))
                    
                    respuesta = await cliente.post("/prestamos/", json={"libro_id": libro_id, "usuario_id": usuario_id})
                    print(respuesta.json())
                case 7:
                    print("\nSeleccionó 'Actualizar préstamos'")
                    await infoPrestamos(cliente)
                    prestamo_id = int(input("Escriba el ID del prestamo a actualizar: "))
                    fecha_dev = input("Escriba la fecha de devolucion (yyyy-mm-dd): ")

                    respuesta = await cliente.put(f"/prestamos/{prestamo_id}", json={"fecha_d": fecha_dev})
                    print(respuesta.json())

                case 8:
                    print("\nSeleccionó 'Consultar préstamos'")
                    await infoPrestamos(cliente)
                case 9:
                    print("\nSeleccionó 'Registar autores'")
                    nombre = str(input("Escriba el nombre del autor: "))
                    nacionalidad = str(input("Escriba la nacionalidad: "))

                    respuesta = await cliente.post("/autores/", json={"nombre": nombre, "nacionalidad": nacionalidad})
                    print(respuesta.json())
                case 10:
                    print("\nSeleccionó 'Ver TOP libros más prestados'")
                    await infoTopLibros(cliente)
                case 11:
                    print("Seleccionó 'SALIR DEL SISTEMA'")
                case _:
                    print("\nOpcion no valida")

if __name__ == "__main__":
    asyncio.run(main())