from cliente.cliente import BUSCAR
from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio

SERVICIO = "busc9" # Buscar

if __name__ == "__main__":
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
        serv, msg=escucharBus(sock)
        if serv != SERVICIO:
            respuesta = {"respuesta":"servicio equivocado"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
        else:
            # Lo que debe hacer el servicio
            diccionario = json.loads(msg) # {"buscarPor": "id_administrador", "buscar": 8}
            if diccionario["buscarPor"] == "id_administrador":
                cursor = conexion.execute("SELECT * FROM local WHERE id_administrador = ?", (diccionario["buscar"],))
                local = cursor.fetchone()
                respuesta = {"respuesta":local}
                enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)
            elif diccionario["buscarPor"] == "comida":
                pass
