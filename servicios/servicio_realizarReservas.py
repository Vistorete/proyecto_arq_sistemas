from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio
import datetime

SERVICIO = "rlrv9" # Buscar
def formatearFecha(dia:str, mes:str, año:str):
    dia = dia.replace(' ','')
    mes = mes.replace(' ','')
    año = año.replace(' ','')

    while len(dia) <2:
        dia = "0"+dia
    while len(mes) <2:
        mes = "0"+mes
    # AAAA-MM-DD
    return año+"-"+mes+"-"+dia

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
            inputCliente = json.loads(msg) # {"id_usuario": 1, "id_local":2, "nombre_usuario":"xd","mes":12,"dia":4,"año"2021}
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
            # Valida la disponibildad:
                if local:
                    fecha = formatearFecha(inputCliente["dia"],inputCliente["mes"],inputCliente["año"])
                    #Verificar si la fecha es valida
                    if datetime.datetime.strptime(fecha,"%Y-%m-%d") > datetime.datetime.today():

                        query_obtener_reservas = "SELECT * FROM reserva WHERE id_local = ? AND fecha = ?"
                        cursor = conexion.execute(query_obtener_reservas,(inputCliente["id_local"],fecha))
                        reservas = cursor.fetchall()
                        if local[-1] > len(reservas):
                            insert_reserva = "INSERT INTO reserva(id_cliente, id_local, fecha) VALUES(?,?,?)"
                            conexion.execute(insert_reserva,(inputCliente["id_usuario"],inputCliente["id_local"],fecha))
                            conexion.commit()
                            respuesta = {"respuesta":"Se ha logrado registrar su reservar para el dia "+fecha}
                            enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)
                        else:
                            respuesta = {"error":"No hay cupos disponibles para ese dia"}
                            enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)
                    else:
                        respuesta={"error":"Error al seleccionar la fecha"}
                        enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
                # respuesta = {"respuesta":"si"}
