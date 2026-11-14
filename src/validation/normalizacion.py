"""Rol A: normalización y estandarización de registros.

SEMANA 10: implementar las funciones marcadas TODO.
Contrato: recibir un diccionario y devolver una COPIA normalizada.
No modificar el registro original.
"""

import copy

def normalizar_registro(registro: dict) -> dict:
    """
    Recibe un diccionario de registro, valida su tipo, crea una copia profunda 
    para no alterar el original y estandariza sus campos clave (id, tipo, valor, unidad).
    Cumple con el contrato para datos provenientes tanto de memoria como de archivos externos.
    """
    # TODO A-S10-01: validar que registro sea un diccionario.
    if not isinstance(registro, dict):
        raise ValueError("El registro debe ser un diccionario.")

    # Crear una copia profunda para evitar modificar el original
    copia = copy.deepcopy(registro)

    # TODO A-S10-02: quitar espacios de id, tipo, unidad y valor textual.
    if "id" in copia and copia["id"] is not None:
        copia["id"] = str(copia["id"]).strip().upper()
        
    if "unidad" in copia and isinstance(copia["unidad"], str):
        # Estandarización unificada de unidades para evitar duplicidad de lógica
        unidad_limpia = copia["unidad"].strip()
        unidad_lower = unidad_limpia.lower()
        if unidad_lower in ["c", "°c", "celsius", "grados"]:
            unidad_limpia = "°C"
        elif unidad_lower in ["%", "porcentaje", "pct"]:
            unidad_limpia = "%"
        elif unidad_lower in ["hpa", "hectopascales"]:
            unidad_limpia = "hPa"
        copia["unidad"] = unidad_limpia

    if "valor" in copia and copia["valor"] is not None:
        valor_raw = copia["valor"]
        if isinstance(valor_raw, str):
            # Limpieza robusta para valores provenientes de archivos (reemplazo de comas decimales)
            valor_raw = valor_raw.strip().replace(",", ".")
        copia["valor"] = valor_raw

    # TODO A-S10-03: estandarizar tipo a minúsculas y limpiar acentos básicos.
    if "tipo" in copia and isinstance(copia["tipo"], str):
        tipo_limpio = copia["tipo"].strip().lower()
        reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
        for acento, sin_acento in reemplazos.items():
            tipo_limpio = tipo_limpio.replace(acento, sin_acento)
        copia["tipo"] = tipo_limpio

    # TODO A-S10-04: devolver una copia normalizada.
    return copia


def normalizar_lote(registros: list[dict]) -> list[dict]:
    """
    Aplica la normalización a una lista completa de registros (ideal para lotes 
    provenientes de archivos CSV, JSON o Excel en las semanas 12 y 13).
    """
    if not isinstance(registros, list):
        raise ValueError("El lote de registros debe ser una lista.")
    
    return [normalizar_registro(reg) for reg in registros if isinstance(reg, dict)]


