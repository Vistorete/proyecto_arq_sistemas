# Librerias de terceros
import mysql.connector as mysqlcn

# Clase que funciona como "envoltorio" para el objeto del conector MySQL
# Los atributos de esta clase corresponden a las credenciales de la base de datos, configuraciones y los objetos
# db y cursor, que son necesarios para realizar la interacción con la base.

class DB:
    def __init__(self):
        # Se asignan a los atributos todas las credenciales al momento de instanciar el objeto
        self.user="admindev@ayudantiaseii "
        self.passwd="2021ayudantias#"
        self.host="ayudantiaseii.mysql.database.azure.com"
        self.port="3306"
        self.database="ayudantias_eii"
        self.autocommit=True

        # Se invoca el método de conexión y se realizan configuraciones en el cursor
        self.db = self.connect()
        self.cursor = self.db.cursor(dictionary=True, buffered=True)
        self.cursor.execute("SET NAMES utf8mb4;")
    
    # Método de conexión a la base de datos mediante el conector MySQL (proveniente de la librería)
    def connect(self):
        return mysqlcn.connect(
            user=self.user,
            passwd=self.passwd,
            host=self.host,
            port=self.port,
            database=self.database,
            autocommit=self.autocommit,
            auth_plugin='mysql_native_password'
        )
    
    # Método para manejar los timeout cuando se ejecutan las consultas
    def query(self, query, values):
        try:
            self._query(query, values)

        except (mysqlcn.errors.InterfaceError, mysqlcn.errors.OperationalError):
            # En caso de que exista algún error de conexión con la base de datos (de interfaz o de operación)
            # al momento de estar realizando una consulta, se reconecta a la base de datos y se procede a
            # realizar la consulta nuevamente.

            self.db = self.connect()
            self.cursor = self.db.cursor(dictionary=True, buffered=True)
            self.cursor.execute("SET NAMES utf8mb4;")
            self._query(query, values)

        return self.cursor
    
    # Método que realiza la consulta a la base de datos como tal
    def _query(self, query, values):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
