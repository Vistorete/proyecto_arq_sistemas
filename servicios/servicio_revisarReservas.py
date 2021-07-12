from os import curdir
import socket
import socket, sys, json
from gestor_base import conexion, crearBase
from funcionesGenerales import enviarTransaccion, escucharBus, registrarServicio
import datetime
SERVICIO = "rvac9" # Buscar

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
            diccionario = json.loads(msg) # {"buscaRol": "admin", "id_usuario": x, "nombre": xxxx, "buscar":x } buscaRol: quien busca, id_buscador:id del cliente o local
            print(diccionario)

            query_usuario=""" SELECT * FROM usuario WHERE id = ? AND nombre= ? AND rol = ?  """
            cursor=conexion.execute(query_usuario,(diccionario["id_usuario"],diccionario["nombre_usuario"],diccionario["buscarPor"]))
            user=cursor.fetchone()
        
            if diccionario['buscarPor'] == "administrador":
                query_obtener_local="SELECT id from local WHERE id_adminstrador= ?"
                cursor= conexion.execute(query_obtener_local,(diccionario["id_usuario"],))
                local=cursor.fetchone()
                query_obtener_reservas = "SELECT reserva.id,usuario.nombre,reserva.fecha FROM reserva JOIN usuario on usuario.id=reserva.id_cliente WHERE fecha >= ? AND id_local = ? ORDER BY fecha ASC"
                cursor = conexion.execute(query_obtener_reservas,(datetime.datetime.now(),local))
                reservas = cursor.fetchall()
                for i in reservas:
                    print(i)
                respuesta = {"reservas":reservas}
                enviarTransaccion(sock, json.dumps(respuesta), SERVICIO)

            elif diccionario['buscarPor']== "cliente":
                query_obtener_reservas= "SELECT reserva.id,local.nombre,local.comuna,fecha FROM reserva JOIN local ON local.id=reserva.id_local WHERE fecha >= ? AND id_cliente= ? ORDER BY fecha ASC"#nombre local
                cursor = conexion.execute(query_obtener_reservas,(datetime.datetime.now(),diccionario['id_usuario']))
                reservas= cursor.fetchall()
                for i in reservas:
                    print(i)
                respuesta={"reservas":reservas}
                enviarTransaccion(sock,json.dumps(respuesta),SERVICIO)