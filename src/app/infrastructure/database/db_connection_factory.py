from psycopg2 import  pool


##SE VA A USAR FACTORY PARA GESTIONAR DE MANERA EFICIENTE LAS CONEXIONES
##FACTORY PROVEERA UNA UNICA INSTANCIA DE CONEXION AQUI SE USAURA SINGLETON conection_pull


class DatabaseConectionFactory:

    ##variable como instancia unica SINGLETON
    _connection_pool = None

    @classmethod
    def initialize (cls , minconn:int = 1, maxconn:int = 5 ):
        if cls._connection_pool is None:
            cls._connection_pool = pool.SimpleConnectionPool(
                minconn,maxconn,
                user= "postgress",
                password = "1234",
                host = "localhost",
                port= "5432",
                database = "postgres"
            )

    ##responsabilidad del programador liberar la conexion despues de ser usada para su reutiliacion
    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            raise Exception("Pool connection not initialized")
        return cls._connection_pool.getconn()

    ##metodo para liberar el pool de conection
    @classmethod
    def release_connection(cls , connection):
        cls._connection_pool.putconn(connection)

    ## Este metodo se levanta cuando se hace un reinicio de la app de FastApi
    @classmethod
    def close_pool(cls):
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            cls._connection_pool = None



