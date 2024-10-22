from db.logger_base import log
from psycopg2 import pool
import sys
from config import settings

class Conexion:

    _DATABASE = settings._DATABASE
    _USERNAME = settings._USERNAME
    _PASSWORD = settings._PASSWORD
    _DB_PORT = settings._DB_PORT
    _HOST = settings._HOST
    _MIN_CON = settings._MIN_CON
    _MAX_CON = settings._MAX_CON
    _pool = settings._pool

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                      host = cls._HOST,
                                                      database = cls._DATABASE,
                                                      user = cls._USERNAME,
                                                      password = cls._PASSWORD,
                                                      port = cls._DB_PORT)
                log.debug(f'Conexión del pool exitosa: {cls._pool}')
                return cls._pool
            except Exception as e:
                log.error(f'Ocurrió un error al obtener el pool: {e}')
                sys.exit
        else:
            return cls._pool

    @classmethod
    def obtenerConexion(cls):
        conexion = cls.obtenerPool().getconn()
        log.debug(f'Conexión de objeto exitosa: {conexion}')
        return conexion

    @classmethod
    def liberarConexion(cls, conexion):
        cls.obtenerPool().putconn(conexion)
        log.debug(f'Regresamos la conexión al pool: {conexion}')

    @classmethod
    def cerrarConexiones(cls):
        cls.obtenerPool().closeall()
        log.debug('Pool de conexiones cerrado')


