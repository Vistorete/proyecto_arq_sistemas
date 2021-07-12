
from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio

SERVICIO = "rvac9" # Buscar

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
            # diccionario = json.loads(msg) # {"buscarPor": "id_administrador", "buscar": 8}
            query_obtener_reservas = "SELECT * FROM reserva WHERE fecha >= '2011-11-01' ORDER BY fecha DESC"
            cursor = conexion.execute(query_obtener_reservas,())
            reservas = cursor.fetchall()
            for i in reservas:
                print(i)
            respuesta = {"reservas":reservas}
            enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)