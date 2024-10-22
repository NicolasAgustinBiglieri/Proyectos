from db.conexion import Conexion
from db.logger_base import log

class CursorDelPool:

    def __init__(self):
        self._conexion = None
        self._cursor = None

    def __enter__(self):
        log.debug(f'Inicio del método with __enter__')
        self._conexion = Conexion.obtenerConexion()
        self._cursor = self._conexion.cursor()
        return self._cursor
    
    def __exit__(self, type_excep, value_excep, traceback_excep):
        log.debug(f'Se ejecuta método __exit__')
        if value_excep:
            self._conexion.rollback()
            log.error(f'Ocurrió un error, se realiza rollback: {type_excep} {value_excep} {traceback_excep}')
        else:
            self._conexion.commit()
            log.debug('Se realiza commit')
        Conexion.liberarConexion(self._conexion)
