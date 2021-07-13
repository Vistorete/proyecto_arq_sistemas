import sqlite3

conexion = sqlite3.connect("bdd2.db")


def crearBase():
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuario(
            id integer primary key autoincrement,
            nombre text,
            rol text
        );
    """)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS local(
            id integer primary key autoincrement,
            id_administrador integer,
            nombre text,
            descripcion text,
            comuna text,
            tipo_comida text,
            reservas_maxima integer,
            horario_inicio text,
            horario_cierre text
        );
    """)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS reserva(
            id integer primary key autoincrement,
            id_cliente integer,
            id_local integer,
            fecha text
        );
    """)
crearBase()