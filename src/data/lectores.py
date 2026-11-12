"""Rol C: lectores de archivos. Implementación del estudiante en semana 12.

Contrato de salida para cada lector: list[dict] con claves id, tipo, valor, unidad.
Los lectores no normalizan ni clasifican: entregan datos crudos al servicio.
"""
def leer_csv(archivo):
    # TODO C-S12-01: leer CSV y devolver lista de diccionarios.
    raise NotImplementedError("Pendiente: lector CSV, semana 12")

def leer_json(archivo):
    # TODO C-S12-02: leer JSON y devolver lista de diccionarios.
    raise NotImplementedError("Pendiente: lector JSON, semana 12")

def leer_excel(archivo):
    # TODO C-S12-03: leer Excel y devolver lista de diccionarios.
    raise NotImplementedError("Pendiente: lector Excel, semana 12")

"""Rol C: lectores de archivos. Implementación del estudiante en semana 12.

Contrato de salida para cada lector: list[dict] con claves id, tipo, valor, unidad.
Los lectores no normalizan ni clasifican: entregan datos crudos al servicio.
"""
import csv
import io
import json
import pandas as pd


def leer_csv(archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-01: leer CSV y devolver lista de diccionarios.
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8-sig", newline="") as f:
            return [dict(row) for row in csv.DictReader(f)]
    
    if isinstance(archivo, io.BytesIO) or hasattr(archivo, "read"):
        contenido = archivo.read()
        if isinstance(contenido, bytes):
            contenido = contenido.decode("utf-8-sig")
        return [dict(row) for row in csv.DictReader(io.StringIO(contenido))]
        
    return [dict(row) for row in csv.DictReader(archivo)]


def leer_json(archivo):
    """Lee un archivo JSON y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-02: leer JSON y devolver lista de diccionarios.
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = json.load(archivo)
    
    if isinstance(datos, dict):
        return [datos]
    return list(datos)


def leer_excel(archivo):
    """Lee un archivo Excel y devuelve una lista de diccionarios con la estructura canónica."""
    # TODO C-S12-03: leer Excel y devolver lista de diccionarios.
    df = pd.read_excel(archivo)
    return df.to_dict(orient="records")