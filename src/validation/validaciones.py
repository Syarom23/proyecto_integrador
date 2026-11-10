"""Rol A: reglas de validación de calidad de registros."""
TIPOS_PERMITIDOS = {"temperatura", "presion", "humedad"}

def validar_registro(registro):
    """Contrato: devuelve (es_valido: bool, motivos: list[str])."""
    # TODO A-S10-05: validar campos obligatorios: id, tipo, valor y unidad.
    
    campos_obligatorios = ["id", "tipo", "valor", "unidad"]
    for campo in campos_obligatorios:
        if campo not in registro or registro[campo] is None or str(registro[campo]).strip() == "":
            motivos.append(f"Falta el campo obligatorio o está vacío: {campo}")

    # TODO A-S10-06: validar tipo permitido.

    tipo = registro.get("tipo")
    if tipo is not None:
        if not isinstance(tipo, str) or tipo.lower() not in TIPOS_PERMITIDOS:
            motivos.append(f"Tipo no permitido o inválido: '{tipo}'. Tipos válidos: {list(TIPOS_PERMITIDOS)}")

    # TODO A-S10-07: validar que valor tenga formato numérico admitido.

    valor = registro.get("valor")
    if valor is not None:
        try:
            # Intentar convertir a float para comprobar si es un número válido
            float(str(valor).strip())
        except (ValueError, TypeError):
            motivos.append(f"El valor no tiene un formato numérico válido: '{valor}'")


    # TODO A-S10-08: definir reglas de unidad por tipo de sensor.

    # Reglas básicas de unidad esperada según el tipo
    unidades_por_tipo = {
        "temperatura": {"celsius", "fahrenheit", "k", "c", "f"},
        "presion": {"hpa", "pa", "bar", "atm", "psi"},
        "humedad": {"%", "percent", "porcentaje"}
        }
    
    unidad = registro.get("unidad")
    if tipo is not None and isinstance(tipo, str) and unidad is not None:
        tipo_lower = tipo.lower()
        unidad_lower = str(unidad).strip().lower()
        if tipo_lower in unidades_por_tipo:
            if unidad_lower not in unidades_por_tipo[tipo_lower]:
                motivos.append(f"Unidad '{unidad}' no corresponde o no es válida para el tipo '{tipo}'")


    # TODO A-S10-09: devolver todos los motivos encontrados, no solo el primero.
    es_valido = len(motivos) == 0
    return es_valido, motivos


    raise NotImplementedError("Pendiente: implementación del rol A, semana 10")
                                  