"""Rol A: reglas de validación de calidad de registros."""
TIPOS_PERMITIDOS = {"temperatura", "presion", "humedad"}


# Reglas centralizadas y unificadas por tipo de sensor (evita duplicidad)
TIPOS_PERMITIDOS = {
    "temperatura": {
        "unidades": {"celsius", "fahrenheit", "k", "c", "f", "°c"},
        "min": -50.0,
        "max": 100.0
    },
    "presion": {
        "unidades": {"hpa", "pa", "bar", "atm", "psi"},
        "min": 300.0,
        "max": 1100.0
    },
    "humedad": {
        "unidades": {"%", "percent", "porcentaje"},
        "min": 0.0,
        "max": 100.0
    },
}

CAMPOS_OBLIGATORIOS = ["id", "tipo", "valor", "unidad"]

def validar_registro(registro: dict) -> tuple[bool, list[str]]:
    """Contrato: devuelve (es_valido: bool, motivos: list[str]).
    Valida campos obligatorios, tipos permitidos, formato numérico (compatible con archivos)
    y coherencia de unidades, acumulando todos los motivos encontrados.
    """
    motivos = []
    
    if not isinstance(registro, dict):
        return False, ["El registro debe ser un diccionario válido."]

    # TODO A-S10-05: validar campos obligatorios: id, tipo, valor y unidad.
    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in registro or registro[campo] is None or str(registro[campo]).strip() == "":
            motivos.append(f"Falta el campo obligatorio o está vacío: {campo}")

    # Si faltan campos obligatorios, salimos temprano para evitar errores de tipo
    if motivos:
        return False, motivos

    # TODO A-S10-06: validar tipo permitido.
    tipo = registro.get("tipo")
    tipo_lower = None
    if tipo is not None:
        if not isinstance(tipo, str):
            motivos.append(f"El tipo debe ser una cadena de texto: '{tipo}'")
            return False, motivos
        
        tipo_lower = tipo.strip().lower()
        # Normalización básica de acentos para evitar rechazos por tildes
        reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
        for acento, sin_acento in reemplazos.items():
            tipo_lower = tipo_lower.replace(acento, sin_acento)

        if tipo_lower not in TIPOS_PERMITIDOS:
            motivos.append(f"Tipo no permitido o inválido: '{tipo}'. Tipos válidos: {list(TIPOS_PERMITIDOS.keys())}")

    # TODO A-S10-07: validar que valor tenga formato numérico admitido (soporta comas de archivos CSV/Excel).
    valor = registro.get("valor")
    valor_convertido = None
    if valor is not None:
        try:
            # Reemplazar coma por punto para tolerar formatos numéricos de archivos externos
            valor_str = str(valor).strip().replace(",", ".")
            valor_convertido = float(valor_str)
        except (ValueError, TypeError):
            motivos.append(f"El valor no tiene un formato numérico válido: '{valor}'")

    # TODO A-S10-08: definir reglas de unidad por tipo de sensor y validación de rangos lógicos.
    unidad = registro.get("unidad")
    if tipo_lower in TIPOS_PERMITIDOS and unidad is not None:
        unidad_lower = str(unidad).strip().lower()
        unidades_validas = TIPOS_PERMITIDOS[tipo_lower]["unidades"]
        
        if unidad_lower not in unidades_validas:
            motivos.append(f"Unidad '{unidad}' no corresponde o no es válida para el tipo '{tipo}'")

        # Validación de rango numérico lógico (útil para pruebas de calidad)
        if valor_convertido is not None:
            min_val = TIPOS_PERMITIDOS[tipo_lower]["min"]
            max_val = TIPOS_PERMITIDOS[tipo_lower]["max"]
            if not (min_val <= valor_convertido <= max_val):
                motivos.append(f"El valor '{valor_convertido}' está fuera del rango lógico para '{tipo}' ({min_val} a {max_val})")

    # TODO A-S10-09: devolver todos los motivos encontrados, no solo el primero.
    es_valido = len(motivos) == 0
    
    return es_valido, motivos 