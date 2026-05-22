from datetime import datetime
from peewee import *

database = MySQLDatabase(
    "bb_db",
    user="root",
    password="",
    host="localhost",
    port=3306
)

class Autor(Model):
    nombre = CharField(max_length=50)
    nacionalidad = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "autor"

class Libro(Model):
    titulo = CharField(max_length=50)
    autor = ForeignKeyField(Autor)
    publicacion = IntegerField()

    class Meta:
        database = database
        table_name = "libro"

class Usuario(Model):
    nombre = CharField(max_length=50)
    matricula = CharField(max_length=9, unique=True)
    contrasena = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "usuario"

class Prestamo(Model):
    libro = ForeignKeyField(Libro)
    usuario = ForeignKeyField(Usuario)
    fecha_p = DateField(default=datetime.now)
    fecha_d = DateField(null=True)

    class Meta:
        database = database
        table_name = "prestamo"