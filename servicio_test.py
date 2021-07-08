# test de servicio
# "sinit" crea el servicio
# transaccion: 
import socket
import sys

SERVICIO = "autenticacion"


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


    # Respuesta de la transaccion
    amount_received = 0
    while True:
        data = sock.recv(4096)
        amount_received += len(data)
        # print('received {!r}'.format(data))
        tamañoTransaccion = int(data[:5].decode())
        print("tamaño de transaccion:",tamañoTransaccion)
        msgTransaccion= data[5:5+tamañoTransaccion]
        print("msg:",msgTransaccion)

def escucharBus(sock):
    pass

def registrarServicio(sock, nombreServicio="test1"):
    enviarTransaccion(sock, "sinit", nombreServicio)

    
    


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

    

    registrarServicio(sock, "regis")
    print('cerrando socket')
    sock.close()