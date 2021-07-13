# test de servicio
# "sinit" crea el servicio
# transaccion: 
from os import curdir
import socket
import datetime
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio,GuardarError

SERVICIO = "logi9" #Registro de usuarios



def loginUsuario(registro):
    print("registrar", registro)
    cursor = conexion.execute("SELECT * FROM usuario WHERE nombre = ?", (registro["usuario"],))
    usuario = cursor.fetchone()
    if usuario:
        print(usuario) # (7, 'nicolas', 'cliente')
        respuesta = {"respuesta":{"id":usuario[0],"usuario":usuario[1],"rol":usuario[2]}}
        enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
    else:
        respuesta = {"respuesta":"noNombre"}
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
        try:
            serv, msg=escucharBus(sock)
            if serv == SERVICIO:
                loginUsuario(json.loads(msg))
            else:
                respuesta = {"respuesta":"servicio equivocado"}
                enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
        except Exception as e:
            datetime_object = datetime.datetime.now()
            GuardarError(e, SERVICIO, datetime_object)
            respuesta = {"error":"No se pudo realizar la solicitud."}
            enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)
            print(e)