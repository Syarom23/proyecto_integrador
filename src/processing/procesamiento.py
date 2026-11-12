"""Orquestación del procesamiento.

Semana 10–12: completar integración con validación y excepciones.
La clasificación permanece centralizada en clasificacion.py.
"""
from src.processing.clasificacion import clasificar_valor

def procesar_registros(registros):
    # TODO B-S10-01: coordinar normalización y validación sin duplicar reglas.
    # TODO B-S10-02: clasificar únicamente registros válidos.
    # TODO B-S10-03: devolver el contrato común definido en docs/contratos_modulos.md.
    # TODO B-S11-04: aislar errores por registro y continuar el lote.
    # TODO B-S12-04: integrar entradas de lectores CSV, JSON y Excel.
    # La función clasificar_valor(valor, tipo) debe reutilizarse.
    raise NotImplementedError("Pendiente: integración del procesamiento, semanas 10–12")


# parte 1 
from src.validation.normalizacion import normalizar_registro
from src.validation.validaciones import validar_registro

def procesar_registros(registros):
    registros_validos = []
    registros_invalidos = []
    errores = []

    for idx, registro in enumerate(registros):
        # TODO B-S10-01: coordinar normalización y validación sin duplicar reglas.
        reg_normalizado = normalizar_registro(registro)
        es_valido, motivos = validar_registro(reg_normalizado)
        
        if not es_valido:
            reg_inv = dict(reg_normalizado)
            reg_inv["motivos"] = motivos
            registros_invalidos.append(reg_inv)
            continue

  # parte 2 
  # TODO B-S10-02: clasificar únicamente registros válidos.
        valor_str = reg_normalizado.get("valor")
        valor_float = float(valor_str)
        
        tipo = reg_normalizado.get("tipo")
        clasificacion = clasificar_valor(valor_float, tipo)
        
        reg_procesado = dict(reg_normalizado)
        reg_procesado["valor"] = valor_float
        reg_procesado["clasificacion"] = clasificacion
        
        registros_validos.append(reg_procesado)
# parte 3 
# Estructura completa con manejo de excepciones por registro:
    for idx, registro in enumerate(registros):
        try:
            reg_normalizado = normalizar_registro(registro)
            es_valido, motivos = validar_registro(reg_normalizado)
            
            if not es_valido:
                reg_inv = dict(reg_normalizado)
                reg_inv["motivos"] = motivos
                registros_invalidos.append(reg_inv)
                continue

            valor_str = reg_normalizado.get("valor")
            valor_float = float(valor_str)
            
            tipo = reg_normalizado.get("tipo")
            clasificacion = clasificar_valor(valor_float, tipo)
            
            reg_procesado = dict(reg_normalizado)
            reg_procesado["valor"] = valor_float
            reg_procesado["clasificacion"] = clasificacion
            
            registros_validos.append(reg_procesado)

        except Exception as e:
            # TODO B-S11-04 & TODO B-S12-04: aislar errores y continuar el lote
            reporte_err = {
                "origen": "procesamiento",
                "identificador": registro.get("id", f"IDX_{idx}") if isinstance(registro, dict) else "DESCONOCIDO",
                "mensaje": str(e),
                "categoria": "EXCEPCION_REGISTRO"
            }
            errores.append(reporte_err)
#parte 4
# TODO B-S10-03: devolver el contrato común definido en docs/contratos_modulos.md.
    resumen = {
        "total_procesados": len(registros),
        "total_validos": len(registros_validos),
        "total_invalidos": len(registros_invalidos),
        "total_errores": len(errores)
    }

    return {
        "registros_validos": registros_validos,
        "registros_invalidos": registros_invalidos,
        "errores": errores,
        "resumen": resumen
    }
      