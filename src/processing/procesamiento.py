"""Orquestación del procesamiento.

Semana 10–12: completar integración con validación y excepciones.
La clasificación permanece centralizada en clasificacion.py.

REVISIÓN (B-1): el archivo conservaba la función de la plantilla (con
`raise NotImplementedError`) y debajo la del estudiante. Además, la versión del
estudiante tenía DOS ciclos `for` sobre los mismos registros («parte 2» y
«parte 3») dentro de la misma función: cada registro se procesaba dos veces y
la demostración en memoria mostraba 24 válidos en lugar de 12. Se dejó un solo
ciclo, el de la «parte 3», que ya tenía el try/except por registro.
"""
# REVISIÓN (B-1): todos los imports al inicio del archivo (PEP 8).
from src.exceptions.errores import (
    EVENTOS_TECNICOS,
    DataLabError,
    ErrorConversionValor,
    ErrorEstructuraRegistro,
    ErrorEventoSensor,
    ErrorFormatoFuente,
    crear_reporte_error,
)
from src.processing.clasificacion import clasificar_valor
from src.processing.resumen import generar_resumen
from src.validation.normalizacion import normalizar_registro
from src.validation.validaciones import validar_registro

ORIGEN_POR_DEFECTO = "procesamiento"


def _identificador(registro, indice):
    """Devuelve un identificador útil para el reporte, aunque el registro esté roto."""
    if isinstance(registro, dict) and registro.get("id") not in (None, ""):
        return str(registro["id"]).strip()
    # Se cuenta desde 1 para que coincida con lo que una persona ve en la tabla.
    return f"REGISTRO_{indice + 1}"


def _origen(registro):
    """REVISIÓN (B-6): el lector (Rol C) anota en `_origen` el archivo de donde
    salió el registro; así el reporte de errores dice de qué archivo viene."""
    if isinstance(registro, dict) and registro.get("_origen"):
        return str(registro["_origen"])
    return ORIGEN_POR_DEFECTO


def _revisar_eventos_tecnicos(registro):
    """REVISIÓN (B-3): detecta fallas TÉCNICAS antes de revisar la calidad.

    Un registro con falla técnica no es «de mala calidad»: el dato no es
    confiable porque falló el origen. Por eso se lanza una excepción (Rol B) en
    lugar de agregar un motivo de validación (Rol A).
    """
    if not isinstance(registro, dict):
        raise ErrorEstructuraRegistro(
            f"El registro no es un diccionario (llegó {type(registro).__name__}: {registro!r})"
        )
    if registro.get("_error_tecnico"):
        fila = registro.get("_fila")
        detalle = f" (fila {fila})" if fila is not None else ""
        raise ErrorEstructuraRegistro(f"{registro['_error_tecnico']}{detalle}")

    evento = registro.get("observacion_tecnica")
    if isinstance(evento, str) and evento.strip().upper().startswith("SIMULACION_"):
        evento = evento.strip().upper()
        clase_error = EVENTOS_TECNICOS.get(evento, ErrorEventoSensor)
        raise clase_error(f"Evento técnico del sensor: {evento}")


def _convertir_valor(valor):
    """REVISIÓN (B-8): conversión controlada a float (TODO B-S12: errores de conversión).

    Si la validación hizo bien su trabajo, esto nunca falla. Pero si alguien
    cambia la validación y deja pasar un valor raro, el error queda reportado
    con su propia categoría (CONVERSION) en lugar de detener el lote.
    `from error` conserva la excepción original como causa (__cause__).
    """
    try:
        return float(valor)
    except (ValueError, TypeError) as error:
        raise ErrorConversionValor(f"No se pudo convertir el valor '{valor}' a número") from error


def procesar_registros(registros):
    # TODO B-S10-01: coordinar normalización y validación sin duplicar reglas.
    # TODO B-S10-02: clasificar únicamente registros válidos.
    # TODO B-S10-03: devolver el contrato común definido en docs/contratos_modulos.md.
    # TODO B-S11-04: aislar errores por registro y continuar el lote.
    # TODO B-S12-04: integrar entradas de lectores CSV, JSON y Excel.
    # La función clasificar_valor(valor, tipo) debe reutilizarse.
    registros_validos = []
    registros_invalidos = []
    errores = []

    # REVISIÓN (B-8): si la entrada completa no es una lista, no hay registros
    # que procesar; se reporta un único error y se devuelve el contrato vacío
    # (con las mismas claves) en lugar de lanzar una excepción.
    if not isinstance(registros, list):
        error = ErrorFormatoFuente(f"Se esperaba una lista de registros y llegó {type(registros).__name__}")
        errores.append(crear_reporte_error(ORIGEN_POR_DEFECTO, "LOTE", error, error.CATEGORIA))
        registros = []

    for indice, registro in enumerate(registros):
        identificador = _identificador(registro, indice)
        try:
            # REVISIÓN (B-3): 1) fallas técnicas -> errores (Rol B).
            _revisar_eventos_tecnicos(registro)

            # 2) calidad del dato -> válidos o inválidos (Rol A).
            reg_normalizado = normalizar_registro(registro)
            es_valido, motivos = validar_registro(reg_normalizado)

            if not es_valido:
                # REVISIÓN (B-4): forma del contrato que consume la interfaz:
                # {"registro": ..., "motivos": [...]}. Antes los motivos se
                # metían DENTRO del registro y la interfaz no los encontraba
                # (buscaba item["registro"] y item["motivos"]).
                registros_invalidos.append({"registro": reg_normalizado, "motivos": motivos})
                continue

            # 3) solo los válidos se convierten y clasifican (TODO B-S10-02).
            valor_float = _convertir_valor(reg_normalizado.get("valor"))

            tipo = reg_normalizado.get("tipo")
            clasificacion = clasificar_valor(valor_float, tipo)

            reg_procesado = dict(reg_normalizado)
            reg_procesado["valor"] = valor_float
            reg_procesado["clasificacion"] = clasificacion

            registros_validos.append(reg_procesado)

        except DataLabError as error:
            # TODO B-S11-04 & TODO B-S12-04: aislar errores y continuar el lote
            # REVISIÓN (B-2): errores PREVISTOS. La categoría la aporta la propia
            # excepción (atributo CATEGORIA). Antes todo era "EXCEPCION_REGISTRO"
            # y el reporte no tenía fecha_hora: la pestaña «Errores técnicos»
            # fallaba al buscar esa columna.
            errores.append(crear_reporte_error(_origen(registro), identificador, error, error.CATEGORIA))
        except Exception as error:
            # REVISIÓN (B-2): red de seguridad para errores IMPREVISTOS (un fallo
            # de programación). Va después: Python usa el primer except que
            # coincide, y Exception coincide con todo.
            errores.append(crear_reporte_error(
                _origen(registro), identificador,
                f"Error inesperado ({type(error).__name__}): {error}", "SISTEMA",
            ))

    # TODO B-S10-03: devolver el contrato común definido en docs/contratos_modulos.md.
    # REVISIÓN (B-7): el resumen se calcula con generar_resumen (módulo común)
    # sobre los registros VÁLIDOS, como dice el contrato. Antes se armaba a mano
    # y no tenía las claves que usan la interfaz y la consola (total, altos,
    # normales, bajos, promedio, por_sensor). Los contadores del estudiante se
    # conservan como información adicional.
    resumen = generar_resumen(registros_validos)
    resumen.update({
        "total_procesados": len(registros),
        "total_validos": len(registros_validos),
        "total_invalidos": len(registros_invalidos),
        "total_errores": len(errores),
    })

    return {
        "registros_validos": registros_validos,
        "registros_invalidos": registros_invalidos,
        "errores": errores,
        "resumen": resumen,
    }
