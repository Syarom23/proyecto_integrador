"""Rol C: selección y unificación de fuentes."""
from src.data.fuentes_memoria import cargar_desde_memoria
from src.data.lectores import leer_csv, leer_json, leer_excel

"""Rol C: lectores de archivos. 

Contrato de salida para cada lector: list[dict] con claves id, tipo, valor, unidad.
Los lectores no normalizan ni clasifican: entregan datos crudos al servicio.
"""
import csv
import io
import json
import pandas as pd

def leer_csv(archivo) -> list[dict]:
    """Lee un archivo CSV y devuelve una lista de diccionarios con la estructura canónica."""
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8-sig", newline="") as f:
            return [dict(row) for row in csv.DictReader(f)]
    
    if isinstance(archivo, io.BytesIO) or hasattr(archivo, "read"):
        contenido = archivo.read()
        if isinstance(contenido, bytes):
            contenido = contenido.decode("utf-8-sig")
        return [dict(row) for row in csv.DictReader(io.StringIO(contenido))]
        
    return [dict(row) for row in csv.DictReader(archivo)]

def leer_json(archivo) -> list[dict]:
    """Lee un archivo JSON y devuelve una lista de diccionarios con la estructura canónica."""
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = json.load(archivo)
    
    if isinstance(datos, dict):
        return [datos]
    return list(datos)

def leer_excel(archivo) -> list[dict]:
    """Lee un archivo Excel y devuelve una lista de diccionarios con la estructura canónica."""
    df = pd.read_excel(archivo)
    return df.to_dict(orient="records")
"""Rol C: selección y unificación de fuentes (Semana 12)."""
try:
    from src.data.fuentes_memoria import cargar_desde_memoria
    from src.data.lectores import leer_csv, leer_json, leer_excel
except ModuleNotFoundError:
    def cargar_desde_memoria():
        print("Advertencia: Usando función de respaldo para cargar_desde_memoria")
        return []

def cargar_datos(archivo=None, nombre_archivo: str = "") -> list[dict]:
    """Carga memoria o delega al lector según extensión."""
    if archivo is None:
        return cargar_desde_memoria()
    
    nombre = nombre_archivo or (archivo if isinstance(archivo, str) else "")
    if "." not in nombre:
        raise ValueError("No se pudo determinar la extensión del archivo.")
        
    extension = nombre.lower().rsplit(".", 1)[-1]
    
    if extension == "csv":
        return leer_csv(archivo)
    if extension == "json":
        return leer_json(archivo)
    if extension in ("xlsx", "xls"):
        return leer_excel(archivo)
        
    raise ValueError(f"Extensión no soportada: {extension}")