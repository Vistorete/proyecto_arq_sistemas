# test
import socket, sys, json
from os import system, name
from funcionesGenerales import limpiarPantalla, enviarTransaccion, escucharBus
REGISTRO = "regi9"
LOGIN = "logi9" #Registro de usuarios
BUSCAR = "busc9"
REGISTRAR_LOCAL = "rglc9"
REVISAR_RESERVAS = "rvac9"

sesion = {"id": None,"usuario":None,"rol":None}
sock = None


def menuLogin():
    # limpiarPantalla()
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Autenticación                                                         ║
    ║ Ingresa tu nombre de usuario                                          ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ vacio para salir                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Nombre de usuario:"""
    #ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhh aqui estoy
    limpiarPantalla()
    nombreUsuario = input(menu)
    if nombreUsuario != "":
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
                global sesion
                sesion=msg["respuesta"]
                print(sesion)
                if sesion["rol"] == "administrador":
                    # Menu admin
                    menuAdmin()
                else:
                    limpiarPantalla()
                    error = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Autenticación                                                         ║
    ║ Lo sentimos, tu rol no pertenece a este cliente                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
        Presiona Enter para continuar..."""
                    input(error)
                    menuIngresar()
    else:
        menuIngresar()
def menuAdmin():
    contenido = {"buscarPor":"id_administrador","buscar":sesion["id"]}
    enviarTransaccion(sock, json.dumps(contenido), BUSCAR )
    serv, mensaje=escucharBus(sock)
    print( serv, mensaje)
    diccionario = json.loads(mensaje[2:])
    print("diccionario",diccionario)
    if diccionario["respuesta"] != None: #{'respuesta': None}
        infoLocal=f"""Información del local:
        Nombre: {diccionario["respuesta"][2]}
        Comuna: {diccionario["respuesta"][4]}
        Descripción: {diccionario["respuesta"][3]}
        Tipo de comida: {diccionario["respuesta"][5]}
        Máximo de reservas: {diccionario["respuesta"][6]}
        Horario:{diccionario["respuesta"][7]}-{diccionario["respuesta"][8]}"""

    else:
        infoLocal=""
    limpiarPantalla()
    menu = f"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Menu administrador de restaurante                                     ║
    ║ Elige una opción                                                      ║
    ║ 1) Registrar Local (Se sobrescribira si ya tiene datos guardados)     ║
    ║ 2) Revisar reservas del restaurante                                   ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ vacio para salir                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    {infoLocal}
    Opción:"""
    opcionElegida = input(menu)
    if opcionElegida == "1":
        menuRegistrarLocal()
        pass
    elif opcionElegida =="2":
        menuReservas()
    else:
        menuIngresar()
    pass

def menuReservas():
    limpiarPantalla()
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Reservas actuales                                                     ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(menu)
    contenido = {"buscarPor": "administrador", "id_usuario":sesion["id"],"nombre_usuario":sesion["usuario"]}
    enviarTransaccion(sock,json.dumps(contenido),REVISAR_RESERVAS)
    serv, mensaje=escucharBus(sock)
    respuesta = json.loads(mensaje[2:])
    resp = respuesta["reservas"]
    # print(respuesta)
    if resp != "":
        for reserva in resp:
            info = f"""            ════════════════════════════════
                ID usuario: {reserva[0]}
                Nombre del cliente: {reserva[1]}
                fecha: {reserva[2]}
    """
            print(info)
        print("            ════════════════════════════════")

        menu2 = """
        ╔═══════════════════════════════════════════════════════════════════════╗
        ║ 1) Eliminar reserva                                                   ║
        ╠═══════════════════════════════════════════════════════════════════════╣
        ║ vacio para salir                                                      ║
        ╚═══════════════════════════════════════════════════════════════════════╝
        Opción:"""
        opcionElegida = input(menu2)
        if opcionElegida != "":
            contenido = {"borrarPor":"administrador","id_usuario":sesion["id"],"nombre_usuario":sesion["usuario"],"metodo":"id","id_reserva":opcionElegida}
            enviarTransaccion(sock,json.dumps(contenido),ELIMINAR)
            serv, mensaje=escucharBus(sock)
            respuesta = json.loads(mensaje[2:])
            resp = respuesta["respuesta"]
            # print(respuesta)
            if resp == "reservas eliminadas":
                menu3 = """
        ╔═══════════════════════════════════════════════════════════════════════╗
        ║ reserva eliminada                                                     ║
        ╚═══════════════════════════════════════════════════════════════════════╝
            """
                opcionElegida = input(menu3)
                menuReservas()
            else:
                menu3 = """
        ╔═══════════════════════════════════════════════════════════════════════╗
        ║ error al eliminar reserva                                             ║
        ╚═══════════════════════════════════════════════════════════════════════╝
            """
                opcionElegida = input(menu3)
                menuReservas()
    else:
        menuAdmin()

def menuRegistrarse():
    nombreUsuario = None
    rol = None
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registro de administrador                                             ║
    ║ Ingresa tu nombre de usuario                                          ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ vacio para salir                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Nombre de usuario:"""

    limpiarPantalla()
    nombreUsuario = input(menu)
    if nombreUsuario !="" :
        rol = "2"
        menu2 = f"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registro                                                              ║
    ║ Confirma tus datos:                                                   ║
    ║ 1) Si                                                                 ║
    ║ 2) No                                                                 ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ vacio para salir                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
        Usuario: {nombreUsuario}
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
            menuIngresar()
        elif confirmar == "2":
            menuRegistrarse()
        else:
            menuIngresar()

    else:
        menuIngresar()

def menuRegistrarLocal():
    limpiarPantalla()
    menu = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║ Proceso cliente para proyecto de Arquitectura de Sistemas             ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ Registrar Local                                                       ║
    ║ Ingresa los siguientes valores separados por una ","                  ║
    ║ 1) Nombre del local                                                   ║
    ║ 2) Descripción del local                                              ║
    ║ 3) Comuna                                                             ║
    ║ 4) Tipo de comida (si son mas de 2 mas separalas con un espacio)      ║
    ║ 5) Máxima cantidad de reservas                                        ║
    ║ 6) Horario apertura                                                   ║
    ║ 7) Horario cierre                                                     ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║ vacio para salir                                                      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    Datos:"""
    datos = input(menu)
    if datos != "":
        datos = datos.replace(", ",",")
        datos = datos.split(",")
        if len(datos) == 7:
            contenido = {
                "id_administrador":sesion["id"],
                "usuario":sesion["usuario"],
                "nombre":datos[0],
                "descripcion":datos[1],
                "comuna":datos[2],
                "tipo_comida":datos[3],
                "reservas_maxima":datos[4],
                "h_inicio":datos[5],
                "h_termino":datos[6]
                }
            enviarTransaccion(sock, json.dumps(contenido), REGISTRAR_LOCAL )
            serv, mensaje=escucharBus(sock)
            msg =  json.loads(mensaje[2:]) # los 2 primeros caracteres son OK
            print(msg)
            menuAdmin()

        else:
            menuAdmin()
    else:
        menuIngresar()
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
        menuRegistrarse()
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
    ###########
    menuIngresar()
