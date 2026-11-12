"""Rol C: adaptador de fuentes en memoria."""
from src.data.sensores import obtener_registros

def cargar_desde_memoria():
    """Fuente de datos funcional desde la primera entrega."""
    return obtener_registros()

def preparar_registros_prueba():
    """Rol C: escenarios adicionales de entrada para pruebas de semana 10."""
    # TODO C-S10-01: construir registros con espacios, mayúsculas y formatos diversos.
    # TODO C-S10-02: construir casos incompletos y tipos no reconocidos.
    # TODO C-S10-03: no alterar los 12 registros base.
    raise NotImplementedError("Pendiente: implementación del rol C, semana 10")

"""Rol C: adaptador de fuentes en memoria (Semana 10)."""
from src.data.sensores import obtener_registros

def cargar_desde_memoria():
    """Fuente de datos funcional desde la primera entrega."""
    return obtener_registros()

def preparar_registros_prueba():
    """Rol C: escenarios adicionales de entrada para pruebas de semana 10."""
    # TODO C-S10-03: no alterar los registros base (trabajamos sobre una copia)
    registros_base = list(obtener_registros())
    
    # TODO C-S10-01: construir registros con espacios, mayúsculas y formatos diversos.
    casos_normalizacion = [
        {"id": "  101 ", "tipo": "  TEMPERATURA  ", "valor": " 23.5 ", "unidad": "  c  "},
        {"id": "102", "tipo": "Humedad", "valor": "68,4", "unidad": " % "},
        {"id": " 103", "tipo": "presion", "valor": "1013.25", "unidad": "HPA"}
    ]
    
    # TODO C-S10-02: construir casos incompletos y tipos no reconocidos.
    casos_invalidos = [
        {"id": 201, "tipo": "temperatura"},  # Faltan claves obligatorias
        {"id": 202, "tipo": "radiacion_gamma", "valor": 15.0, "unidad": "Sv"},  # Tipo no reconocido
        {"id": 203, "tipo": "temperatura", "valor": "texto_invalido", "unidad": "C"},  # Valor no numérico
        {None, "", None, ""}  # Caso nulo / extremo
    ]
    
    return registros_base + casos_normalizacion + casos_invalidos