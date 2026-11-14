"""Rol C: adaptador de fuentes en memoria (Semana 10).

REVISIÓN (C-1): el archivo contenía la plantilla original (con
`raise NotImplementedError`) y debajo la versión del estudiante: el import, el
docstring y las dos funciones estaban repetidos. Se dejó una sola versión.
"""
from src.data.sensores import obtener_registros


def cargar_desde_memoria():
    """Fuente de datos funcional desde la primera entrega."""
    return obtener_registros()


def preparar_registros_prueba():
    """Rol C: escenarios adicionales de entrada para pruebas de semana 10.

    Son datos de MALA CALIDAD o con formato variado: el Rol A los normaliza y
    los acepta o los rechaza con motivos.
    """
    # TODO C-S10-03: no alterar los registros base (trabajamos sobre una copia)
    registros_base = list(obtener_registros())

    # TODO C-S10-01: construir registros con espacios, mayúsculas y formatos diversos.
    casos_normalizacion = [
        {"id": "  101 ", "tipo": "  TEMPERATURA  ", "valor": " 23.5 ", "unidad": "  c  "},
        {"id": "102", "tipo": "Humedad", "valor": "68,4", "unidad": " % "},
        {"id": " 103", "tipo": "presion", "valor": "1013.25", "unidad": "HPA"},
        # REVISIÓN (C-3): dos variantes más que el Rol A debe estandarizar:
        # tipo con tilde ("Presión") e id en minúsculas.
        {"id": "p104", "tipo": "Presión", "valor": 1008, "unidad": "hPa"},
    ]

    # TODO C-S10-02: construir casos incompletos y tipos no reconocidos.
    casos_invalidos = [
        {"id": 201, "tipo": "temperatura"},  # Faltan claves obligatorias
        {"id": 202, "tipo": "radiacion_gamma", "valor": 15.0, "unidad": "Sv"},  # Tipo no reconocido
        {"id": 203, "tipo": "temperatura", "valor": "texto_invalido", "unidad": "C"},  # Valor no numérico
        # REVISIÓN (C-3): antes este caso era {None, "", None, ""}. Con llaves y
        # SIN «clave: valor» Python crea un SET (conjunto), no un diccionario, y
        # además elimina los repetidos: quedaba {None, ""}. Un set no es un
        # registro, así que no probaba la calidad sino la estructura. Ahora es
        # un diccionario con todos los campos vacíos, que es lo que se buscaba.
        {"id": None, "tipo": "", "valor": None, "unidad": ""},  # Caso nulo / extremo
        # REVISIÓN (C-3): valor fuera del rango plausible (centinela 999).
        {"id": 205, "tipo": "humedad", "valor": 999, "unidad": "%"},
    ]

    return registros_base + casos_normalizacion + casos_invalidos


def preparar_escenarios_defectuosos():
    """REVISIÓN (C-4): escenarios de FUENTES DEFECTUOSAS (Rol C, semana 11).

    No hay que confundirlos con los datos de mala calidad de
    preparar_registros_prueba(): aquí el problema no es el dato, sino que la
    fuente falló o entregó algo con forma incorrecta. El Rol B debe reportarlos
    como errores técnicos sin detener el lote.

    Devuelve 2 registros correctos y 4 defectuosos.
    """
    return [
        {"id": "T901", "tipo": "temperatura", "valor": 21.0, "unidad": "°C"},
        # Evento técnico simulado por el sensor.
        {"id": "T902", "tipo": "temperatura", "valor": 22.0, "unidad": "°C",
         "observacion_tecnica": "SIMULACION_TIMEOUT_SENSOR"},
        # Fila que el lector marcó como irregular (como lo hace leer_csv).
        {"id": "T903", "_error_tecnico": "Fila con columnas de más o de menos",
         "_origen": "memoria", "_fila": 4},
        # Un texto en lugar de un diccionario.
        "T904,temperatura,23,°C",
        # Un registro que no llegó.
        None,
        {"id": "H901", "tipo": "humedad", "valor": 55.0, "unidad": "%"},
    ]


# REVISIÓN (C-4): prueba manual protegida con `if __name__ == "__main__"`.
# Este bloque solo se ejecuta al correr el archivo directamente, nunca cuando
# otro módulo lo importa (Streamlit, pruebas, consola). Para probar a mano:
#     python -m src.data.fuentes_memoria
if __name__ == "__main__":
    print(len(cargar_desde_memoria()), "registros base")
    print(len(preparar_registros_prueba()), "registros de prueba")
    print(len(preparar_escenarios_defectuosos()), "escenarios defectuosos")
