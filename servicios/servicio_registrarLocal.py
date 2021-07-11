# test de servicio
# "sinit" crea el servicio
# transaccion: 
from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio

SERVICIO = "rglc9" #Registro de usuarios
BUSCAR = "busc9"

if __name__ == "__main__":
    # Conexion con el bus
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('Servicio: Conectandose a {} puerto {}'.format(*server_address))
        sock.connect(server_address)
    # En caso de error cierra la aplicacion
    except: 
        print("no se pudo conectar con el bus")
        quit() 

    registrarServicio(sock, SERVICIO)
    while True:
        # try:
        serv, msg=escucharBus(sock) 
        print(serv, msg) #{{"id_administrador": 8, "nombre": "Los Pollos Hermanos", "descripcion": "Basado en BrBa", "comuna": "Condado de colorado", "tipo_comida": "china peruana", "reservas_maxima": "20"}}
            # Valida al usuario
        msg = json.loads(msg)
        cursor = conexion.execute("SELECT * FROM usuario WHERE id = ? AND rol = 'administrador'", (msg["id_administrador"],))
        usuario = cursor.fetchone()
        print("Servicio: Usuario",usuario)
        if usuario:
            # Revisa si ya tiene un local
            cursor = conexion.execute("SELECT * FROM local WHERE id_administrador = ?", ( msg["id_administrador"],))
            local = cursor.fetchone()
            # Si no hay local lo inserta

            if local != None:
                cursor = conexion.execute("INSERT INTO local(id_administrador,nombre, descripcion,comuna,tipo_comida,reservas_maxima) VALUES(?,?,?,?,?,?)",(msg["id_administrador"],msg["nombre"],msg["descripcion"], msg["comuna"].lower(), msg["tipo_comida"],int(msg["reservas_maxima"])))
                conexion.commit()
                respuesta = {"respuesta":"Se registrado correctamente"}
                enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
            # Si hay local lo actualiza



                    

        # except: # Maneja errores
        #     pass
        # Los pollos hermanos, Basado en BrBa, Quilicura, china peruana, 10