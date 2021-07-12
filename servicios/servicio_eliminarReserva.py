from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio
import datetime
SERVICIO = "dlrv9" #ELIMINAR_RESERVAS

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
        if serv != SERVICIO:
            respuesta = {"respuesta":"servicio equivocado"}
            enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
        else:
            diccionario = json.loads(msg) # {"rol": "admin"/"cliente", "borrarPor": "id"/"todo","id":id cliente/local, "id_reserva":id de reserva}

            if diccionario["rol"] == "admin":
                query_obtener_local= """SELECT id FROM local WHERE id_administrador = ?"""
                cursor=conexion.execute(query_obtener_local,(diccionario["id"],))
                local=cursor.fetchone()
                
                if diccionario["borrarPor"]=="id":#el admin borra una reserva mediante el id_reserva.
                    query_borrar_reservas_local="""DELETE FROM reservas WHERE id = ? and id_local = ?"""
                    cursor=conexion.execute(query_borrar_reservas_local,(diccionario["id_reserva"],local))

                elif diccionario["borrarPor"]=="todo":#el admin borra todas las reservas de su local
                    query_borrar_reservas_local= "DELETE FROM reservas WHERE id_local = ?"
                    cursor=conexion.execute(query_borrar_reservas_local,(local,))

                

            elif diccionario["rol"] == "cliente":
                if diccionario["borraPor"]== "id":
                
                    query_borrar_reservas_local=""" DELETE FROM reservas WHERE id = ? AND id_cliente = ?"""
                    cursor=conexion.execute(query_borrar_reservas_local,(diccionario["id_reserva"],diccionario["id"]))
                
                elif diccionario["borraPor"]== "todo":

                    query_borrar_reservas_local="""DELETE FROM reservas WHERE id_cliente = ?"""
                    cursor=conexion.execute(query_borrar_reservas_local,(diccionario["id"],))
            
        respuesta={'respuesta':"reservas eliminadas"}
        enviarTransaccion(sock,json.dumps(respuesta),SERVICIO)