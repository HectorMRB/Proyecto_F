import requests

url = "http://127.0.0.1:8000"

def infoUsuarios():
    respuesta = requests.get(f"{url}/usuariosL/")
    print("\n==================== Mostrando lista de usuarios ====================")
    for usuario in respuesta.json():
        print(f"ID: {usuario.get("id")} - Nombre: {usuario.get("nombre")} - Matricula: {usuario.get("matricula")} - Contrasena: {usuario.get("contrasena")}")
    print("======================================================================\n")

def infoLibros():
    respuesta = requests.get(f"{url}/librosL/")
    print("\n============ Mostrando lista de libros ============")
    for libro in respuesta.json():
        print(f"ID: {libro.get("id")} - Titulo: {libro.get("titulo")} - Autor: {libro.get("autor_id")} - Publicacion: {libro.get("publicacion")}")
    print("==================================================\n")

def infoPrestamos():
    respuesta = requests.get(f"{url}/prestamosL/")
    print("\n============ Mostrando lista de prestamos ============")
    for prestamo in respuesta.json():
        print(f"ID: {prestamo.get("id")} - Libro: {prestamo.get("libro_id")} - Usuario: {prestamo.get("usuario_id")} - Fecha prestamo: {prestamo.get("fecha_p")} - Fecha devolucion: {prestamo.get("fecha_d")}")
    print("==================================================\n")

def infoAutor():
    autores = requests.get(f"{url}/autoresL/")
    print("\n============ Mostradno lista de autores ============")
    for autor in autores.json():
        print(f"ID: {autor.get("id")} - Nombre: {autor.get("nombre")} - nacionalidad: {autor.get("nacionalidad")}")
    print("==================================================\n")

def infoTopLibros():
    respuesta = requests.get(f"{url}/libros/top")
    print("\n==================== TOP LIBROS MÁS PRESTADOS ====================")
    for item in respuesta.json():
        print(f"ID Libro: {item.get('libro_id')} - Cantidad de Préstamos: {item.get('cantidad_prestamos')}")
    print("==================================================================\n")


def main():
    print("\n==== Bienvenido al sistema de la biblioteca central ====")
    eleccion = 0

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
        print("11) SALIR DEL SISTEMA")
        print("====== MENU ======\n")

        eleccion = int(input("Digite su opcion: "))

        match eleccion:
            case 1:
                print("\nSeleccionó 'Registrar libros'")
                nombre = input("Escriba el nombre: ")

                infoAutor()

                autor = int(input("Escriba el ID del autor: "))
                publicacion = int(input("Escriba el año de publicacion: "))

                respuesta = requests.post(f"{url}/libros/", json={"titulo": nombre, "autor_id": autor, "publicacion": publicacion})

                print(respuesta.json())

            case 2:
                print("\nSeleccionó 'Consultar libros'")
                infoLibros()
            case 3:
                print("\nSeleccionó 'Actualizar libros'")

                infoLibros()

                libro_id = int(input("Escriba el ID del libro a actualizar: "))
                titulo = input("Escriba el titulo del libro a actualizar: ")

                autores = requests.get(f"{url}/autoresL/")
                print("===== Mostradno lista de autores =====")
                print(f"{autores.json()}\n")

                autor = int(input("Escriba el id del autor del libro a actualizar: "))
                publicacion = int(input("Escriba el publicacion del libro a actualizar: "))

                datos={}

                if titulo:
                    datos["titulo"] = titulo
                if autor:
                    datos["autor_id"] = autor
                if publicacion:
                    datos["publicacion"] = publicacion

                respuesta = requests.put(f"{url}/libros/{libro_id}", json=datos)
                print(respuesta.json())


            case 4:
                print("\nSelecciono 'Resitrar usuarios'")

                nombre = input("Escriba el nombre del usuario: ")
                matricula = input("Escriba la matricual del usuario: ")
                contrasena = input("Contraseña: ")

                respuesta = requests.post(f"{url}/usuarios/", json={"nombre":nombre, "matricula": matricula, "contrasena": contrasena})

                print(respuesta.json())
            case 5:
                print("\nSeleccionó 'Consultar usuarios'")
                infoUsuarios()

            case 6:
                print("\nSeleccionó 'registrar préstamos'")

                infoLibros()
                libro_id = int(input("Escriba el ID del libro a registrar: "))

                infoUsuarios()
                usuario_id = int(input("Escriba el ID del usuario a registrar: "))
                respuesta = requests.post(f"{url}/prestamos/", json={"libro_id": libro_id, "usuario_id": usuario_id})
                print(respuesta.json())
            case 7:
                print("\nSeleccionó 'Actualizar préstamos'")
                infoPrestamos()
                prestamo_id = int(input("Escriba el ID del prestamo a actualizar: "))
                fecha_dev = input("Escriba el fecha de devolucion (yyyy-mm-dd): ")

                respuesta = requests.put(f"{url}/prestamos/{prestamo_id}", json={"fecha_d": fecha_dev})

                print(respuesta.json())

            case 8:
                print("\nSeleccionó 'Consultar préstamos'")
                infoPrestamos()
            case 9:
                print("\nSeleccionó 'Registar autores'")
                nombre = str(input("Escriba el nombre del autor: "))
                nacionalidad = str(input("Escriba el nacionalidad: "))

                respuesta = requests.post(f"{url}/autores/", json={"nombre": nombre, "nacionalidad": nacionalidad})
                print(respuesta.json())
            case 10:
                print("\nSeleccionó 'Ver TOP libros más prestados'")
                infoTopLibros()
            case 11:
                print("Seleccionó 'SALIR DEL SISTEMA'")
            case _:
                print("\nOpcion no valida")

if __name__ == "__main__":
    main()