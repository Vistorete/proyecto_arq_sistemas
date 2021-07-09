# test
import socket
import sys

def limpiarPantalla():
    print(chr(27)+'[2j')




def enviarTransaccion(sock,contenido, servicio):
    # Generacion de la transaccion
    # validacion de argumentos
    if len(servicio) < 5 or len(contenido) < 1:
        print("Servicio: Los argumentos no cumplen con los requerimietos")
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


def menuLogin():
    menu = """
╔═══════════════════════════════════════════════════════════════════════╗
║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
╠═══════════════════════════════════════════════════════════════════════╣
║ Bienvenido al sistema                                                 ║
║ Elige una opción:                                                     ║
║ 1) Ingresar                                                           ║
║ 2) Registrarse                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
Opción:"""
    opcionElegida = input(menu)
    if opcionElegida == "1":
        print("ingresar")
    elif opcionElegida =="2":
        print("registrarse")
    else:
        print("No valido")
        menuLogin()







if __name__ == "__main__":
    # Conexion con el bus
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sock.connect(server_address)
    # En caso de error cierra la aplicacion
    except: 
        print("no se pudo conectar con el bus")
        quit()

    

