"""Rol A: normalización y estandarización de registros.

SEMANA 10: implementar las funciones marcadas TODO.
Contrato: recibir un diccionario y devolver una COPIA normalizada.
No modificar el registro original.
"""

import copy

# REVISIÓN (A-8): tabla de equivalencias de unidades.
# El estudiante ya estandarizaba las unidades con una cadena if/elif; aquí se
# conservan exactamente las mismas variantes, pero en un diccionario.
# Ventaja: para aceptar una variante nueva basta con agregar UNA línea, sin
# tocar la lógica. Las claves están en minúsculas porque se buscan con lower().
EQUIVALENCIAS_UNIDAD = {
    "c": "°C", "°c": "°C", "ºc": "°C", "celsius": "°C", "grados": "°C",
    "%": "%", "porcentaje": "%", "pct": "%",
    "hpa": "hPa", "hectopascales": "hPa",
}

# REVISIÓN (A-8): tabla de tildes. str.maketrans + translate reemplaza todos los
# caracteres en una sola pasada (el estudiante usaba un ciclo con replace,
# que también es correcto; este es el modismo de Python para el mismo fin).
SIN_TILDES = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")


def _es_nan(valor) -> bool:
    """REVISIÓN (A-3): detecta NaN (Not a Number).

    NaN es el único valor de Python que NO es igual a sí mismo, por eso
    `valor != valor` solo es verdadero para NaN. Así no hace falta importar
    math ni pandas en el módulo de calidad.
    """
    return isinstance(valor, float) and valor != valor


def normalizar_registro(registro: dict) -> dict:
    """
    Recibe un diccionario de registro, valida su tipo, crea una copia profunda
    para no alterar el original y estandariza sus campos clave (id, tipo, valor, unidad).
    Cumple con el contrato para datos provenientes tanto de memoria como de archivos externos.
    """
    # TODO A-S10-01: validar que registro sea un diccionario.
    if not isinstance(registro, dict):
        # En el flujo integrado nunca se llega aquí: el Rol B revisa la
        # estructura del registro antes de normalizar (ver procesamiento.py).
        raise ValueError("El registro debe ser un diccionario.")

    # Crear una copia profunda para evitar modificar el original
    copia = copy.deepcopy(registro)

    # REVISIÓN (A-3): un NaN (por ejemplo, de una celda vacía de Excel) se
    # convierte en None para que la validación lo reporte como «campo faltante»
    # y no como «valor no numérico». Defensa en profundidad: el lector del
    # Rol C ya evita los NaN, pero el Rol A no debe depender de eso.
    for campo in ("id", "tipo", "valor", "unidad"):
        if _es_nan(copia.get(campo)):
            copia[campo] = None

    # TODO A-S10-02: quitar espacios de id, tipo, unidad y valor textual.
    if "id" in copia and copia["id"] is not None:
        copia["id"] = str(copia["id"]).strip().upper()

    if "unidad" in copia and isinstance(copia["unidad"], str):
        # Estandarización unificada de unidades para evitar duplicidad de lógica
        unidad_limpia = copia["unidad"].strip()
        # REVISIÓN (A-8): la búsqueda en la tabla reemplaza el if/elif.
        # Si la unidad no está en la tabla se deja tal como llegó (sin espacios):
        # normalizar NO es aceptar cualquier cosa; la validación decidirá.
        clave = unidad_limpia.lower().replace(" ", "")
        copia["unidad"] = EQUIVALENCIAS_UNIDAD.get(clave, unidad_limpia)

    if "valor" in copia and copia["valor"] is not None:
        valor_raw = copia["valor"]
        if isinstance(valor_raw, str):
            valor_raw = valor_raw.strip()
            # REVISIÓN (A-7): la coma decimal solo se reemplaza si hay exactamente
            # UNA coma y NINGÚN punto ("21,5" -> "21.5"). Antes se reemplazaban
            # todas las comas, y "1.013,2" se volvía "1.013.2". Regla conservadora:
            # ante la duda, no se inventa el dato y la validación lo rechaza.
            if valor_raw.count(",") == 1 and "." not in valor_raw:
                valor_raw = valor_raw.replace(",", ".")
        # El valor sigue siendo texto: la conversión a float la hace el Rol B
        # después de validar (TODO A-S10-04: solo normalizar).
        copia["valor"] = valor_raw

    # TODO A-S10-03: estandarizar tipo a minúsculas y limpiar acentos básicos.
    if "tipo" in copia and isinstance(copia["tipo"], str):
        # REVISIÓN (A-8): mismo resultado que el ciclo de reemplazos original,
        # usando la tabla SIN_TILDES definida arriba.
        copia["tipo"] = copia["tipo"].strip().lower().translate(SIN_TILDES)

    # TODO A-S10-04: devolver una copia normalizada.
    return copia


def normalizar_lote(registros: list[dict]) -> list[dict]:
    """
    Aplica la normalización a una lista completa de registros (ideal para lotes
    provenientes de archivos CSV, JSON o Excel en las semanas 12 y 13).

    REVISIÓN (A-8): esta función es una utilidad; el procesamiento integrado
    (Rol B) normaliza registro por registro para poder aislar los errores.
    Ojo: aquí los elementos que no son diccionarios se OMITEN en silencio; por
    eso procesar_registros no la usa (un registro no debe perderse sin reporte).
    """
    if not isinstance(registros, list):
        raise ValueError("El lote de registros debe ser una lista.")

    return [normalizar_registro(reg) for reg in registros if isinstance(reg, dict)]
