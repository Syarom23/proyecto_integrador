"""Rol A: normalización y estandarización de registros.

SEMANA 10: implementar las funciones marcadas TODO.
Contrato: recibir un diccionario y devolver una COPIA normalizada.
No modificar el registro original.
"""

def normalizar_registro(registro):
    # TODO A-S10-01: validar que registro sea un diccionario.
    if not isinstance(registro, dict):
        raise ValueError("El registro debe ser un diccionario")

    # Crear una copia para evitar modificar el original
    copia = registro.copy()

    # TODO A-S10-02: quitar espacios de id, tipo, unidad y valor textual.
    if "id" in copia and isinstance(copia["id"], str):
        copia["id"] = copia["id"].strip()
        
    if "unidad" in copia and isinstance(copia["unidad"], str):
        copia["unidad"] = copia["unidad"].strip()
        
    if "valor" in copia and isinstance(copia["valor"], str):
        copia["valor"] = copia["valor"].strip()

    # TODO A-S10-03: estandarizar tipo a minúsculas.
    if "tipo" in copia and isinstance(copia["tipo"], str):
        copia["tipo"] = copia["tipo"].strip().lower()

    # TODO A-S10-04: devolver una copia; no convertir aún el valor a float aquí.
    return copia
  
raise NotImplementedError("Pendiente: implementación del rol A, semana 10")  