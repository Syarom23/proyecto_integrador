"""Rol C: selección y unificación de fuentes (Semana 12).

REVISIÓN (C-1): este archivo contenía una COPIA completa de los tres lectores
(leer_csv, leer_json, leer_excel) y los importaba DOS veces desde lectores.py
(antes y después de las copias). El orden decidía cuál versión se usaba: las
copias reemplazaban a las del primer import y el segundo import las volvía a
reemplazar. Eran código muerto, pero quien leía el archivo no podía saber cuál
versión se ejecutaba. Ahora los lectores existen en un solo lugar
(lectores.py) y este módulo solo elige cuál usar.
"""
from pathlib import Path

from src.data.fuentes_memoria import cargar_desde_memoria
from src.data.lectores import leer_csv, leer_excel, leer_json
from src.exceptions.errores import ErrorFormatoFuente

# REVISIÓN (C-1): se eliminó el bloque try/except ModuleNotFoundError que
# definía un cargar_desde_memoria «de respaldo» que devolvía []. Ocultar un
# error de importación es peligroso: la aplicación parecía funcionar, pero sin
# datos y sin explicar por qué. Si falta un módulo, el error debe verse.

# REVISIÓN (C-8): tabla extensión -> lector (reemplaza la cadena de if).
# Se quitó "xls": el proyecto instala openpyxl, que solo lee .xlsx; aceptar
# .xls prometía algo que después fallaba con un error poco claro.
LECTORES_POR_EXTENSION = {
    "csv": leer_csv,
    "json": leer_json,
    "xlsx": leer_excel,
}


def cargar_datos(archivo=None, nombre_archivo: str = "") -> list[dict]:
    """Carga memoria o delega al lector según extensión."""
    if archivo is None:
        return cargar_desde_memoria()

    # REVISIÓN (C-8): si no se indica el nombre, se toma del propio archivo:
    # `.name` en los archivos de Streamlit o la ruta si es str/Path.
    nombre = nombre_archivo or getattr(archivo, "name", "") or (
        str(archivo) if isinstance(archivo, (str, Path)) else ""
    )
    extension = Path(nombre).suffix.lower().lstrip(".")

    lector = LECTORES_POR_EXTENSION.get(extension)
    if lector is None:
        # REVISIÓN (C-8): ErrorFormatoFuente (contrato de excepciones del
        # proyecto) en lugar de ValueError genérico.
        soportadas = ", ".join("." + e for e in LECTORES_POR_EXTENSION)
        raise ErrorFormatoFuente(
            f"No se puede leer '{nombre or 'archivo sin nombre'}': extensión no soportada. Use {soportadas}."
        )
    return lector(archivo)
