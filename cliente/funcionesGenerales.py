# Cliente
import socket, sys, json
from os import system, name
def limpiarPantalla():
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

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
    # print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())

def escucharBus(sock):
    cantidadRecibida = 0
    tamañoTransaccion = None # Cantidad esperada
    msgTransaccion = ""

    while True:
        data = sock.recv(4096)
        
        if cantidadRecibida == 0:
            tamañoTransaccion = int(data[:5].decode())
            nombreServicio = data[5:10].decode()
            msgTransaccion = msgTransaccion + data[10:].decode()
            cantidadRecibida += len(data)-5
        else:
            msgTransaccion = msgTransaccion + data.decode()
            cantidadRecibida += len(data)

        if cantidadRecibida >= tamañoTransaccion:
            break
        
    return nombreServicio, msgTransaccion