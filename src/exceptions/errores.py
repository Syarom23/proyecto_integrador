"""Rol B: excepciones y registro de incidencias.

Los tipos de excepción y el contrato de reporte están definidos.
El estudiante implementa la estrategia de captura, clasificación y reporte
durante las semanas 11 y 12.
"""
class DataLabError(Exception):
    """Excepción base de la aplicación."""

class ErrorValidacion(DataLabError):
    """El registro no cumple las reglas de calidad."""

class ErrorFormatoFuente(DataLabError):
    """La estructura de entrada no corresponde al contrato esperado."""

class ErrorLecturaFuente(DataLabError):
    """No fue posible leer una fuente de datos."""

def crear_reporte_error(origen, identificador, mensaje, categoria="PROCESAMIENTO"):
    # TODO B-S11-01: construir un diccionario de error normalizado.
    # TODO B-S11-02: incluir fecha/hora y categoría sin ocultar el mensaje original.
    # TODO B-S11-03: evitar que el error de un registro interrumpa el lote completo.
    raise NotImplementedError("Pendiente: implementación del rol B, semanas 11–12")
 
#parte 1 
class DataLabError(Exception):
    """Excepción base de la aplicación."""
    pass

class ErrorValidacion(DataLabError):
    """El registro no cumple las reglas de calidad."""
    pass

class ErrorFormatoFuente(DataLabError):
    """La estructura de entrada no corresponde al contrato esperado."""
    pass

class ErrorLecturaFuente(DataLabError):
    """No fue posible leer una fuente de datos."""
    pass

class ErrorConversionValor(DataLabError):
    """Se lanza cuando el valor de un registro no puede convertirse al formato esperado."""
    pass
parte 2 
from datetime import datetime

def crear_reporte_error(origen, identificador, mensaje, categoria="PROCESAMIENTO"):
    """
    Construye un diccionario de error normalizado incluyendo la fecha/hora actual
    y la categoría, preservando el mensaje original sin alterarlo.
    """
    return {
        "origen": origen,
        "identificador": identificador,
        "mensaje": str(mensaje),
        "categoria": categoria,
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
parte 3 
def normalizar_registro(registro):
    """
    Normaliza un registro individual asegurando consistencia básica.
    """
    if not isinstance(registro, dict):
        return registro
    
    registro_copia = dict(registro)
    if "valor" in registro_copia and isinstance(registro_copia["valor"], str):
        registro_copia["valor"] = registro_copia["valor"].strip()
    return registro_copia

def validar_registro(registro):
    """
    Valida las reglas de calidad de un registro ya normalizado.
    Retorna un booleano y una lista con los motivos en caso de fallo.
    """
    motivos = []
    if not isinstance(registro, dict):
        motivos.append("El registro no es un diccionario válido")
        return False, motivos
        
    if "id" not in registro or not registro["id"]:
        motivos.append("Falta el identificador 'id'")
        
    if "valor" not in registro:
        motivos.append("Falta el campo 'valor'")
    
    es_valido = len(motivos) == 0
    return es_valido, motivos
parte 4 
def procesar_lote_registros(registros):
    """
    Procesa un conjunto de registros aplicando normalización, validación y tipado.
    Registra los errores de manera estructurada sin interrumpir la cola.
    """
    resultados = []
    errores_detectados = []

    for idx, registro in enumerate(registros):
        identificador = f"indice_{idx}"
        try:
            # 1. Validación de estructura de la fuente
            if not isinstance(registro, dict):
                raise ErrorFormatoFuente("La estructura de entrada no corresponde al contrato esperado.")
            
            # Normalizar datos
            registro_norm = normalizar_registro(registro)
            identificador = registro_norm.get("id", identificador)
            
            # 2. Validación de datos internos
            es_valido, motivos = validar_registro(registro_norm)
            if not es_valido:
                raise ErrorValidacion(f"El registro no cumple con las reglas de calidad: {motivos}")
            
            # 3. Tratamiento y conversión segura del valor
            valor_str = registro_norm.get("valor")
            try:
                valor_float = float(valor_str)
                if valor_float < 0:
                    raise ErrorValidacion("El valor numérico no puede ser menor a cero.")
                registro_norm["valor"] = valor_float
            except (ValueError, TypeError) as conversion_error:
                raise ErrorConversionValor(f"Fallo de conversión a float para el valor '{valor_str}': {conversion_error}")

            # Si supera exitosamente el flujo, lo guardamos
            resultados.append({"id": identificador, "registro": registro_norm, "estado": "exitoso"})

        except DataLabError as e:
            # Captura controlada de excepciones de nuestra firma
            reporte = crear_reporte_error(
                origen="procesar_lote_registros",
                identificador=identificador,
                mensaje=e,
                categoria="CALIDAD_DATOS"
            )
            errores_detectados.append(reporte)
            
        except Exception as e:
            # Captura de errores de ejecución generales inesperados
            reporte = crear_reporte_error(
                origen="procesar_lote_registros",
                identificador=identificador,
                mensaje=f"Error inesperado: {str(e)}",
                categoria="PROCESAMIENTO"
            )
            errores_detectados.append(reporte)

    return resultados, errores_detectados
parte 5 
# Lote de pruebas con diferentes escenarios
lote_prueba = [
    {"id": "REG-001", "valor": " 450.70 "},     # Válido con espacio en blanco
    {"id": "REG-002", "valor": -10},             # Inválido (Valor negativo)
    "no_es_un_diccionario",                     # Inválido (Formato incorrecto)
    {"id": "REG-003", "valor": "no_numerico"},   # Inválido (Conversión float)
    {"id": "REG-004"}                           # Inválido (Falta valor)
]

correctos, fallidos = procesar_lote_registros(lote_prueba)

print("=== REGISTROS PROCESADOS CON ÉXITO ===")
for r in correctos:
    print(r)

print("\n=== REPORTES DE ERROR GENERADOS ===")
for e in fallidos:
    print(e)
