# test de servicio
# "sinit" crea el servicio
# transaccion: 
import socket
import socket, sys, json
from typing import Counter
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio
SERVICIO = "regi9" #Registro de usuarios


    
    
def registrarUsuario(registro):
    print("registrar", registro)
    # Validar que el usuario no exista
    cursor = conexion.execute("SELECT nombre FROM usuario WHERE nombre = ?", (registro["usuario"],))
    resultado = cursor.fetchone()
    if resultado == None: # Inicia el proceso de registro
        if registro["rol"] in ["1","2"]:
            rol = "cliente" if registro["rol"] == "1" else "administrador"
            conexion.execute("INSERT INTO usuario (nombre, rol) VALUES(?,?)",(registro["usuario"],rol))
            conexion.commit()
            respuesta = {"respuesta":"Se registrado correctamente"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
        else:
            respuesta = {"respuesta":"No se ha podido registrar al usuario"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
    else: # si el usuario ya esta registrado
        respuesta = {"respuesta":"El usuario ya está registrado"}
        enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)


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
        serv, msg=escucharBus(sock)
        print(serv, msg)
        if serv == SERVICIO:
            registrarUsuario(registro=json.loads(msg))
        else:
            respuesta = {"respuesta":"servicio equivocado"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)

    print('cerrando socket')
    sock.close()
    