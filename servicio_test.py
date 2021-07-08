# test de servicio
# "sinit" crea el servicio
# transaccion: 
import socket
import sys

SERVICIO = "auten" #autenticacion


def enviarTransaccion(sock, servicio, contenido):
    # Generacion de la transaccion
    # validacion de argumentos
    if len(servicio) < 5 or len(contenido) < 1:
        print("los argumentos no cumplen con los requerimietos")
        return
    # contruccion de la transaccion
    largoTransaccion = str(len(contenido) + 5)
    while len(largoTransaccion) <5:
        largoTransaccion = "0" + largoTransaccion

    transaccion = largoTransaccion + servicio + contenido
    print("transaccion:",transaccion)
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

def registrarServicio(sock, nombreServicio="test1"):
    enviarTransaccion(sock, "sinit", nombreServicio)
    serv, msg = escucharBus(sock)
    if serv =="sinit" and msg[:2]=="OK":
        print("servicio iniciado con exito")
    else:
        print("no se pudo iniciar el servicio")
    
    


if __name__ == "__main__":
    # Conexion con el bus
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('conectandose a {} puerto {}'.format(*server_address))
        sock.connect(server_address)
    # En caso de error cierra la aplicacion
    except: 
        print("no se pudo conectar con el bus")
        quit() 

    

    registrarServicio(sock, SERVICIO)
    while True:
        serv, msg=escucharBus(sock)
        if serv == SERVICIO:
            print(msg)
            sock.sendall("probando".encode())

    print('cerrando socket')
    sock.close()