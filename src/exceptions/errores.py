"""Rol B: excepciones y registro de incidencias.

Los tipos de excepción y el contrato de reporte están definidos.
El estudiante implementa la estrategia de captura, clasificación y reporte
durante las semanas 11 y 12.

REVISIÓN (B-5): el archivo tenía la plantilla original y debajo la solución del
estudiante («parte 1» a «parte 5»), así que cada clase y crear_reporte_error
estaban definidas DOS veces. Python no da error: la segunda definición
reemplaza a la primera en silencio. Se dejó una sola versión de cada una.
"""
from datetime import datetime, timezone

# REVISIÓN (B-5): el import estaba a mitad del archivo («parte 2»). PEP 8 pide
# que todas las importaciones vayan al inicio del módulo.


# ---------------------------------------------------------------------------
# Jerarquía de excepciones
# ---------------------------------------------------------------------------
# REVISIÓN (B-2): cada clase declara su CATEGORIA como atributo de clase. Así el
# procesamiento no necesita una cadena de if/elif para decidir la categoría:
# cada excepción «sabe» la suya y las subclases la heredan o la redefinen.
# Los nombres de categoría coinciden con los que espera la interfaz y las
# pruebas del docente (por ejemplo, TIMEOUT_SENSOR y ESTRUCTURA_REGISTRO).

class DataLabError(Exception):
    """Excepción base de la aplicación."""
    CATEGORIA = "PROCESAMIENTO"


class ErrorValidacion(DataLabError):
    """El registro no cumple las reglas de calidad."""
    CATEGORIA = "VALIDACION"


class ErrorFormatoFuente(DataLabError):
    """La estructura de entrada no corresponde al contrato esperado."""
    CATEGORIA = "FORMATO_FUENTE"


class ErrorLecturaFuente(DataLabError):
    """No fue posible leer una fuente de datos."""
    CATEGORIA = "LECTURA_FUENTE"


class ErrorConversionValor(DataLabError):
    """Se lanza cuando el valor de un registro no puede convertirse al formato esperado."""
    CATEGORIA = "CONVERSION"


# REVISIÓN (B-3): excepciones nuevas para la semana 11 y 12.
class ErrorEstructuraRegistro(ErrorFormatoFuente):
    """Un registro individual llegó roto: no es un diccionario o el lector lo
    marcó con `_error_tecnico` (por ejemplo, una fila CSV con columnas de más).
    Hereda de ErrorFormatoFuente porque es un problema de forma, pero afecta a
    UN registro y no a todo el archivo."""
    CATEGORIA = "ESTRUCTURA_REGISTRO"


class ErrorEventoSensor(DataLabError):
    """El origen informó una falla técnica del sensor (columna observacion_tecnica)."""
    CATEGORIA = "EVENTO_SENSOR"


class ErrorTimeoutSensor(ErrorEventoSensor):
    """El sensor no respondió a tiempo."""
    CATEGORIA = "TIMEOUT_SENSOR"


class ErrorPaqueteIncompleto(ErrorEventoSensor):
    """El paquete de datos del sensor llegó incompleto."""
    CATEGORIA = "PAQUETE_INCOMPLETO"


class ErrorLecturaIntermitente(ErrorEventoSensor):
    """La lectura del sensor fue intermitente y no es confiable."""
    CATEGORIA = "LECTURA_INTERMITENTE"


# REVISIÓN (B-3): tabla de eventos técnicos -> clase de excepción.
# Agregar un evento nuevo es agregar UNA línea; el ciclo de procesamiento no
# cambia. Un evento SIMULACION_* que no esté aquí usa ErrorEventoSensor.
EVENTOS_TECNICOS = {
    "SIMULACION_TIMEOUT_SENSOR": ErrorTimeoutSensor,
    "SIMULACION_PAQUETE_INCOMPLETO": ErrorPaqueteIncompleto,
    "SIMULACION_LECTURA_INTERMITENTE": ErrorLecturaIntermitente,
}


# ---------------------------------------------------------------------------
# Reporte de incidencias
# ---------------------------------------------------------------------------
def crear_reporte_error(origen, identificador, mensaje, categoria="PROCESAMIENTO"):
    """
    Construye un diccionario de error normalizado incluyendo la fecha/hora actual
    y la categoría, preservando el mensaje original sin alterarlo.
    """
    # TODO B-S11-01: construir un diccionario de error normalizado.
    # TODO B-S11-02: incluir fecha/hora y categoría sin ocultar el mensaje original.
    # TODO B-S11-03: evitar que el error de un registro interrumpa el lote completo.
    #   (B-S11-03 se cumple en procesamiento.py: cada registro tiene su try/except.)
    return {
        # REVISIÓN (B-8): identificador va primero: es el orden de columnas de
        # la pestaña «Errores técnicos» (identificador, categoria, origen, ...).
        "identificador": identificador,
        "categoria": categoria,
        "origen": origen,
        "mensaje": str(mensaje),
        # REVISIÓN (B-8): fecha y hora en UTC y formato ISO 8601, como indica
        # el README («fecha/hora UTC»). datetime.now() sin zona horaria depende
        # del reloj del equipo y no se puede comparar entre equipos.
        "fecha_hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# REVISIÓN (B-5): se eliminaron de este archivo:
#   - «parte 3»: copias de normalizar_registro y validar_registro. Son funciones
#     del Rol A (src/validation/); tenerlas aquí duplicaba reglas y, como tenían
#     el mismo nombre, podían confundirse con las verdaderas.
#   - «parte 4»: procesar_lote_registros, una segunda versión del procesamiento
#     que ya vive en src/processing/procesamiento.py (una sola fuente de verdad).
#   - «parte 5»: un lote de prueba con print(). Todo lo que está en el nivel
#     superior de un módulo se ejecuta al importarlo. Hoy procesamiento.py SÍ
#     importa este módulo (antes no lo hacía: por eso las excepciones del Rol B
#     nunca se usaban), así que esos print() habrían aparecido en Streamlit y en
#     las pruebas. Para probar a mano, use el bloque de abajo:
#         python -m src.exceptions.errores
if __name__ == "__main__":
    from src.processing.procesamiento import procesar_registros

    lote_prueba = [
        {"id": "REG-001", "tipo": "presion", "valor": " 450.70 ", "unidad": "hPa"},
        "no_es_un_diccionario",
        {"id": "REG-003", "tipo": "humedad", "valor": "no_numerico", "unidad": "%"},
        {"id": "REG-004", "tipo": "temperatura", "valor": 21, "unidad": "°C",
         "observacion_tecnica": "SIMULACION_TIMEOUT_SENSOR"},
    ]
    resultado = procesar_registros(lote_prueba)
    for error in resultado["errores"]:
        print(error)
