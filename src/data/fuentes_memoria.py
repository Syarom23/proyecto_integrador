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

"""Rol C: lectores de archivos. Implementación del estudiante en semana 12.

Contrato de salida para cada lector: list[dict] con claves id, tipo, valor, unidad.
Los lectores no normalizan ni clasifican: entregan datos crudos al servicio.
"""
import csv
import json
import pandas as pd

def leer_csv(archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios con la estructura canónica."""
    registros = []
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(dict(row))
    else:
        reader = csv.DictReader(archivo)
        for row in reader:
            registros.append(dict(row))
    return registros[cite: 5, 9]

def leer_json(archivo):
    """Lee un archivo JSON y devuelve una lista de diccionarios con la estructura canónica."""
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = json.load(archivo)
    
    if isinstance(datos, dict):
        return [datos]
    return list(datos)[cite: 5, 9]

def leer_excel(archivo):
    """Lee un archivo Excel y devuelve una lista de diccionarios con la estructura canónica."""
    df = pd.read_excel(archivo)
    return df.to_dict(orient="records")[cite: 5, 9]

import csv
import json
import pandas as pd


def leer_csv(archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios con la estructura canónica."""
    import csv
    registros = []
    if isinstance(archivo, (str, bytes)):
        with open(archivo, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(dict(row))
    else:
        reader = csv.DictReader(archivo)
        for row in reader:
            registros.append(dict(row))
    return registros

def leer_json(archivo):
    """Lee un archivo JSON y devuelve una lista de diccionarios con la estructura canónica."""
    import json
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
    import pandas as pd
    df = pd.read_excel(archivo)
    return df.to_dict(orient="records")

   
try:
    from src.data.fuentes_memoria import cargar_desde_memoria
except ModuleNotFoundError:
    def cargar_desde_memoria():
            print("Advertencia: Usando función de respaldo para cargar_desde_memoria")
            return []

def cargar_datos(archivo=None, nombre_archivo=""):
    """Carga memoria o delega al lector según extensión."""
    if archivo is None:
        return cargar_desde_memoria()
    
    extension = nombre_archivo.lower().rsplit(".", 1)[-1]
    
    if extension == "csv":
        return leer_csv(archivo)
    if extension == "json":
        return leer_json(archivo)
    if extension in ("xlsx", "xls"):
        return leer_excel(archivo)
        
    raise ValueError(f"Extensión no soportada: {extension}")


"""Rol C: selección y unificación de fuentes."""
# Eliminamos la importación de src ya que las funciones están definidas localmente en este notebook.
# Si 'cargar_desde_memoria' está en otro archivo, asegúrate de que esté en el directorio actual.
try:
    from src.data.fuentes_memoria import cargar_desde_memoria
except ModuleNotFoundError:
    # Definición temporal en caso de no contar con el paquete src en el entorno de Colab
    def cargar_desde_memoria():
        print("Advertencia: Usando función mock de cargar_desde_memoria")
        return []

def cargar_datos(archivo=None, nombre_archivo=""):
    """Carga memoria o delega al lector según extensión."""
    if archivo is None:
        return cargar_desde_memoria()
    extension = nombre_archivo.lower().rsplit(".", 1)[-1]
    if extension == "csv":
        return leer_csv(archivo)
    if extension == "json":
        return leer_json(archivo)
    if extension in ("xlsx", "xls"):
        return leer_excel(archivo)
    raise ValueError(f"Extensión no soportada: {extension}")


"""Rol C: selección y unificación de fuentes."""
# Las funciones leer_csv, leer_json y leer_excel ya se definieron localmente en el notebook.
try:
    from src.data.fuentes_memoria import cargar_desde_memoria
except ModuleNotFoundError:
    # Definición de respaldo si no existe el módulo src
    def cargar_desde_memoria():
        print("Advertencia: Usando función de respaldo para cargar_desde_memoria")
        return []

def cargar_datos(archivo=None, nombre_archivo=""):
    """Carga memoria o delega al lector según extensión."""
    if archivo is None:
        return cargar_desde_memoria()
    extension = nombre_archivo.lower().rsplit(".", 1)[-1]
    if extension == "csv":
        return leer_csv(archivo)
    if extension == "json":
        return leer_json(archivo)
    if extension in ("xlsx", "xls"):
        return leer_excel(archivo)
    raise ValueError(f"Extensión no soportada: {extension}")