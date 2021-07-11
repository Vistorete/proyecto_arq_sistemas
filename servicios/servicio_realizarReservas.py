from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio

SERVICIO = "rlrv9" # Buscar

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
        print("Servicio:",serv, msg)
        if serv != SERVICIO:
            respuesta = {"respuesta":"servicio equivocado"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
        else:
            inputCliente = json.loads(msg) # {"id_usuario": 1, "id_local":2, "nombre_usuario":"xd","fecha":"24/12/13"}
            # Validar usuario:
            query_validar_usuario = "SELECT * FROM usuario WHERE id = ? AND nombre = ? AND rol ='cliente'"
            cursor = conexion.execute(query_validar_usuario,(inputCliente["id_usuario"],inputCliente["nombre_usuario"]))
            usuario = cursor.fetchone()
            print("Servicio: usuario", usuario)
            # Si el usuario es valid
            if usuario:
            # Hay que validar la existencia del local
                query_validar_local = "SELECT * FROM local WHERE id = ?"
                cursor = conexion.execute(query_validar_local, (int(inputCliente["id_local"]),))
                local = cursor.fetchone()
                print("Servicio: local", local)
                respuesta = {"respuesta":"si"}
                enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)

            
