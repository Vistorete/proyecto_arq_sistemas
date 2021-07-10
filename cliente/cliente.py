# test
import socket, sys, json
from os import system, name
REGISTRO = "regi9"
LOGIN = "logi9" #Registro de usuarios
BUSCAR = "busc9"

sesion = {"id": None,"usuario":None,"rol":None}

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
        # # print("data ricibida:",cantidadRecibida)
        # # print('received {!r}'.format(data))
        # tamañoTransaccion = int(data[:5].decode())
        # nombreServicio = data[5:10].decode()
        # msgTransaccion= data[10:5+tamañoTransaccion].decode()
        # # print("tamaño de transaccion:",tamañoTransaccion)
        # # print("msg:",msgTransaccion)
        
    return nombreServicio, msgTransaccion


def menuIngresar():
    limpiarPantalla()
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
        menuLogin()
    elif opcionElegida =="2":
        menuRegistrarse1()
    else:
        print("No valido")
        menuLogin()



def menuRegistrarse2():
    limpiarPantalla()
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registro                                                              ║
    ║ Elige un rol:                                                         ║
    ║ 1) Cliente                                                            ║
    ║ 2) Administrador                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Rol:"""
    rol = input(menu)
    if rol in ["1","2"]:
        return rol
    else:
        return menuRegistrarse2()

def menuRegistrarse1():
    nombreUsuario = None
    rol = None
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registro                                                              ║
    ║ Ingresa tu nombre de usuario                                          ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Nombre de usuario:"""
    
    limpiarPantalla()
    nombreUsuario = input(menu)
    rol = menuRegistrarse2()
    menu2 = f"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registro                                                              ║
    ║ Confirma tus datos:                                                   ║
    ║ 1) Si                                                                 ║
    ║ 2) No                                                                 ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Usuario: {nombreUsuario}
    Rol: {"Cliente" if rol == "1" else "Administrador"}
    Opción:"""
    limpiarPantalla()
    confirmar = input(menu2)
    if confirmar == "1":
        contenido = {"usuario": nombreUsuario, "rol":rol}
        enviarTransaccion(sock, json.dumps(contenido), REGISTRO )
        serv, mensaje=escucharBus(sock)
        msg =  json.loads(mensaje[2:]) # los 2 primeros caracteres son OK
        print("serv",serv)
        print("msg",msg)
        if serv == REGISTRO:
            if msg["respuesta"]:
                print(msg["respuesta"])
    else:
        menuRegistrarse1()

def menuLogin():
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Autenticación                                                         ║
    ║ Ingresa tu nombre de usuario                                          ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Nombre de usuario:"""
    limpiarPantalla()
    nombreUsuario = input(menu)
    contenido = {"usuario": nombreUsuario}
    enviarTransaccion(sock, json.dumps(contenido), LOGIN )
    serv, mensaje=escucharBus(sock) # msg: {'respuesta': {'id': 1, 'usuario': 'weebtor', 'rol': 'cliente'}}
    msg =  json.loads(mensaje[2:]) # los 2 primeros caracteres son OK
    # print(serv, msg)
    if serv == LOGIN:
        if msg["respuesta"] == "noNombre":
            input("No se ha encontrado el usuario, presione Enter para continuar")
            menuLogin() 
        else:
            # print(msg["respuesta"])
            sesion=msg["respuesta"]
            print(sesion)
            if sesion["rol"] == "cliente":
                # Menu cliente
                pass
            elif sesion["rol"] == "administrador":
                # Menu admin
                pass
            pass
    # if serv == LOGIN:
    #     if msg["respuesta"]:
    #         print(msg["respuesta"])

def menuCliente():
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Menu cliente                                                          ║
    ║ Elige una opción                                                      ║
    ║ 1) Buscar local                                                       ║
    ║ 2) Revisar reservas                                                   ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Opción:"""
    opcionElegida = input(menu)
    if opcionElegida == "1":
        menuBuscarLocal()
        pass
    elif opcionElegida =="2":
        pass
    else:
        menuCliente()
    pass

def menuBuscarLocal():
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Menu cliente                                                          ║
    ║ Ingresa que tipo de comida buscas                                     ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Comida:"""
    comida = input(menu)
    if len(comida)>0:
        contenido = {"buscarPor":"comida","buscar":comida}
        enviarTransaccion(sock, json.dumps(contenido), BUSCAR )
        serv, mensaje=escucharBus(sock)
        msg =  json.loads(mensaje[2:]) # los 2 primeros caracteres son OK

    else:
        menuBuscarLocal
    
def menuAdmin():
    
    pass

sock = None

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
    ###########
    menuIngresar()

    

