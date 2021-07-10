# test de servicio
# "sinit" crea el servicio
# transaccion: 
from os import curdir
import socket
import socket, sys, json

from gestor_base import conexion, crearBase

SERVICIO = "logi9" #Registro de usuarios


def enviarTransaccion(sock,contenido, servicio=SERVICIO):
    # Generacion de la transaccion
    # validacion de argumentos
    if len(servicio) < 5 or len(contenido) < 1:
        print("Servicio: Los argumentos no cumplen con los requerimientos")
        return
    # contruccion de la transaccion
    largoTransaccion = str(len(contenido) + 5)
    while len(largoTransaccion) <5:
        largoTransaccion = "0" + largoTransaccion

    transaccion = largoTransaccion + servicio + contenido
    print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())
    
def escucharBus(sock):
    cantidadRecibida = 0
    
    while True:
        data = sock.recv(4096)
        cantidadRecibida += len(data)
        # print("data ricibida:",cantidadRecibida)
        # print('received {!r}'.format(data))
        tamañoTransaccion = int(data[:5].decode())
        nombreServicio = data[5:10].decode()
        msgTransaccion= data[10:5+tamañoTransaccion].decode()
        # print("tamaño de transaccion:",tamañoTransaccion)
        # print("msg:",msgTransaccion)
        return nombreServicio, msgTransaccion

def registrarServicio(sock):
    enviarTransaccion(sock, SERVICIO,"sinit")
    crearBase()
    serv, msg = escucharBus(sock)
    if serv =="sinit" and msg[:2]=="OK":
        print("Servicio: Servicio iniciado con exito")
    else:
        print("Servicio: No se pudo iniciar el servicio")

def loginUsuario(registro):
    print("registrar", registro)
    cursor = conexion.execute("SELECT * FROM usuario WHERE nombre = ?", (registro["usuario"],))
    usuario = cursor.fetchone()
    if usuario:
        print(usuario)
        respuesta = {"respuesta":"Si hay usuario"}
        enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
    else:
        respuesta = {"respuesta":"No hay usuario con ese nombre"}
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

    registrarServicio(sock)

    while True:
        serv, msg=escucharBus(sock)
        if serv == SERVICIO:
            loginUsuario(json.loads(msg))
        else:
            respuesta = {"respuesta":"servicio equivocado"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)