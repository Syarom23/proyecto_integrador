"""Rol C: lectores de archivos. Implementación del estudiante en semana 12.

Contrato de salida para cada lector: list[dict] con claves id, tipo, valor, unidad.
Los lectores no normalizan ni clasifican: entregan datos crudos al servicio.

REVISIÓN (C-1): el archivo tenía la plantilla (con `raise NotImplementedError`)
y debajo la versión del estudiante; el docstring y las tres funciones estaban
repetidos. Se dejó una sola versión, con los imports al inicio (PEP 8).

REVISIÓN (C-7): además de los datos de cada fila, los lectores agregan dos
metadatos de trazabilidad: `_origen` (nombre del archivo) y `_fila` (número de
fila o posición). Empiezan con «_» para indicar que no son datos del sensor;
la interfaz los muestra como «origen» y «fila».
"""
import csv
import io
import json
import zipfile
from pathlib import Path

import pandas as pd

from src.exceptions.errores import ErrorFormatoFuente, ErrorLecturaFuente

COLUMNAS_OBLIGATORIAS = ("id", "tipo", "valor", "unidad")


# ---------------------------------------------------------------------------
# Funciones auxiliares compartidas por los tres lectores
# ---------------------------------------------------------------------------
def _obtener_bytes(archivo) -> bytes:
    """REVISIÓN (C-7): patrón ADAPTADOR. Convierte cualquier entrada en bytes.

    Antes, si `archivo` era una ruta se usaba open() y si no, .read(). Pero
    cuando el archivo es bytes, open(b"...") lo interpreta como RUTA y falla, y
    un archivo ya leído una vez devuelve b"" en el segundo .read(). Con este
    adaptador los tres lectores trabajan siempre sobre el mismo tipo (bytes).
    """
    if isinstance(archivo, (str, Path)):
        try:
            return Path(archivo).read_bytes()
        except OSError as error:  # FileNotFoundError, PermissionError, ...
            raise ErrorLecturaFuente(f"No fue posible abrir el archivo '{archivo}': {error}") from error
    if isinstance(archivo, (bytes, bytearray)):
        return bytes(archivo)
    # Duck typing: no importa la clase, sino que tenga el método.
    if hasattr(archivo, "getvalue"):  # Streamlit UploadedFile, io.BytesIO
        return archivo.getvalue()
    if hasattr(archivo, "read"):  # archivo abierto con open(..., "rb") o "r"
        contenido = archivo.read()
        return contenido.encode("utf-8") if isinstance(contenido, str) else contenido
    raise ErrorFormatoFuente(f"Tipo de entrada no soportado por los lectores: {type(archivo).__name__}")


def _obtener_texto(archivo) -> str:
    """Decodifica como UTF-8 quitando el BOM (buena decisión del estudiante: utf-8-sig)."""
    try:
        return _obtener_bytes(archivo).decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ErrorLecturaFuente(f"El archivo no está codificado en UTF-8: {error}") from error


def _nombre_origen(archivo, por_defecto: str) -> str:
    """Nombre corto del archivo para la trazabilidad (`_origen`)."""
    nombre = getattr(archivo, "name", None) or (archivo if isinstance(archivo, (str, Path)) else None)
    return Path(str(nombre)).name if nombre else por_defecto


def _verificar_columnas(columnas, origen: str) -> None:
    """REVISIÓN (C-6): un archivo sin las columnas del contrato no se puede
    procesar fila por fila: es un error de la FUENTE completa."""
    faltantes = [c for c in COLUMNAS_OBLIGATORIAS if c not in columnas]
    if faltantes:
        raise ErrorFormatoFuente(f"{origen}: faltan las columnas obligatorias {faltantes}")


# ---------------------------------------------------------------------------
# Lectores
# ---------------------------------------------------------------------------
def leer_csv(archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-01: leer CSV y devolver lista de diccionarios.
    # REVISIÓN (C-7): antes `open(archivo)` también se usaba con bytes, y el
    # caso final `csv.DictReader(archivo)` nunca podía alcanzarse correctamente.
    origen = _nombre_origen(archivo, "CSV")
    lector = csv.DictReader(io.StringIO(_obtener_texto(archivo), newline=""))
    if not lector.fieldnames:
        raise ErrorFormatoFuente(f"{origen}: el archivo CSV está vacío")
    _verificar_columnas(lector.fieldnames, origen)

    registros = []
    # La fila 1 es el encabezado; los datos empiezan en la 2.
    for numero_fila, fila in enumerate(lector, start=2):
        registro = dict(fila)
        # REVISIÓN (C-6): DictReader guarda las columnas SOBRANTES bajo la clave
        # None y rellena las FALTANTES con None. Esa fila no es confiable: se
        # marca con `_error_tecnico` (para que el Rol B la reporte) y la lectura
        # continúa. Una fila rota no debe impedir leer las demás.
        if None in registro or None in registro.values():
            registro.pop(None, None)
            registro["_error_tecnico"] = "Fila irregular: número de columnas distinto al encabezado"
        registro["_origen"] = origen
        registro["_fila"] = numero_fila
        registros.append(registro)
    return registros


def leer_json(archivo):
    """Lee un archivo JSON y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-02: leer JSON y devolver lista de diccionarios.
    origen = _nombre_origen(archivo, "JSON")
    try:
        datos = json.loads(_obtener_texto(archivo))
    except json.JSONDecodeError as error:
        raise ErrorLecturaFuente(f"{origen}: JSON mal formado (línea {error.lineno}): {error.msg}") from error

    # REVISIÓN (C-2): presion.json tiene la forma {"registros": [...]}. Antes,
    # cualquier diccionario se envolvía en una lista ([datos]), así que todo el
    # archivo se trataba como UN registro sin id, tipo, valor ni unidad.
    # Resultado: 708 lecturas se perdían y la interfaz mostraba 1 inválido.
    if isinstance(datos, dict) and isinstance(datos.get("registros"), list):
        datos = datos["registros"]
    elif isinstance(datos, dict) and "id" in datos:
        datos = [datos]  # un único registro suelto (idea original del estudiante)
    if not isinstance(datos, list):
        raise ErrorFormatoFuente(
            f"{origen}: se esperaba una lista de registros o {{\"registros\": [...]}}, "
            f"y se encontró {type(datos).__name__}"
        )

    registros = []
    for posicion, elemento in enumerate(datos, start=1):
        if isinstance(elemento, dict):
            registro = dict(elemento)
        else:
            # REVISIÓN (C-6): un elemento que no es objeto se marca, no se descarta.
            registro = {"_error_tecnico": f"Elemento no es un objeto JSON: {elemento!r}"}
        registro["_origen"] = origen
        registro["_fila"] = posicion
        registros.append(registro)
    return registros


def leer_excel(archivo):
    """Lee un archivo Excel y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-03: leer Excel y devolver lista de diccionarios.
    origen = _nombre_origen(archivo, "Excel")
    try:
        df = pd.read_excel(
            io.BytesIO(_obtener_bytes(archivo)),
            # REVISIÓN (C-5): sin estas dos opciones pandas convertía las celdas
            # vacías y el texto "NA"/"N/A" en NaN, y convertía columnas a float.
            # Los otros lectores entregan "" y "N/A" como texto: la salida debe
            # ser HOMOGÉNEA. El lector no interpreta los datos; decidir qué
            # significa "N/A" le corresponde al Rol A.
            dtype=object,
            keep_default_na=False,
        )
    except (ValueError, zipfile.BadZipFile, OSError) as error:
        raise ErrorLecturaFuente(f"{origen}: no es un archivo Excel (.xlsx) legible: {error}") from error

    _verificar_columnas(df.columns, origen)
    registros = df.to_dict(orient="records")
    # La fila 1 de la hoja es el encabezado; los datos empiezan en la 2.
    for numero_fila, registro in enumerate(registros, start=2):
        registro["_origen"] = origen
        registro["_fila"] = numero_fila
    return registros
