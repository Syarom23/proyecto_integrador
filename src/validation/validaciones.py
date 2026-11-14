"""Rol A: reglas de validación de calidad de registros."""
import math

# REVISIÓN (A-1): el archivo definía TIPOS_PERMITIDOS DOS veces (primero como
# set y luego como diccionario). En Python la segunda asignación reemplaza a la
# primera sin avisar, así que la primera línea era código muerto y confundía.
# Ahora existe una sola tabla de reglas (una sola fuente de verdad).
#
# REVISIÓN (A-1): cada tipo admite UNA unidad canónica. Antes se aceptaban
# fahrenheit, k, pa, bar, atm o psi; pero clasificar_valor() usa umbrales en
# °C, hPa y %, de modo que 70 °F (21 °C, NORMAL) se habría clasificado ALTO.
# La normalización (normalizacion.py) ya convierte "c", "celsius", "HPA", etc.
# a la forma canónica; aquí solo se compara.
#
# REVISIÓN (A-4): rangos de PLAUSIBILIDAD. Responden «¿el dato es creíble?»;
# no clasifican (eso sigue centralizado en clasificar_valor). Se eligieron a
# partir de los datasets: las lecturas normales están entre 2 y 42 °C,
# 851 y 1080 hPa, y 5 y 95 %; los valores centinela (999, -25, 68, 650, 1500,
# 150, ...) quedan fuera. Los rangos anteriores (-50..100 °C y 300..1100 hPa)
# dejaban pasar 68 y 75 °C o 650 y 700 hPa como si fueran mediciones reales.
REGLAS_POR_TIPO = {
    "temperatura": {"unidad": "°C", "min": -10.0, "max": 50.0},
    "presion": {"unidad": "hPa", "min": 800.0, "max": 1100.0},
    "humedad": {"unidad": "%", "min": 0.0, "max": 100.0},
}

# Se conserva el nombre TIPOS_PERMITIDOS que usaba el código original.
TIPOS_PERMITIDOS = set(REGLAS_POR_TIPO)

CAMPOS_OBLIGATORIOS = ["id", "tipo", "valor", "unidad"]


def _esta_vacio(contenido) -> bool:
    """REVISIÓN (A-3): un campo está vacío si es None, texto en blanco o NaN.

    Antes NaN no se consideraba vacío: str(nan) es "nan", que no está en blanco.
    """
    if contenido is None:
        return True
    if isinstance(contenido, str) and contenido.strip() == "":
        return True
    # NaN es el único valor distinto de sí mismo.
    return isinstance(contenido, float) and contenido != contenido


def _a_numero(valor):
    """REVISIÓN (A-5): devuelve el float si `valor` es un número admitido; si no, None.

    - bool se rechaza: en Python True y False son int (True == 1).
    - "nan", "inf" e "infinity" se rechazan: float() los acepta, pero no son
      mediciones. Antes float("nan") pasaba como un número válido.
    - No se reemplaza la coma: eso es responsabilidad de la normalización
      (antes se hacía en los dos módulos: regla duplicada).
    """
    if isinstance(valor, bool):
        return None
    try:
        numero = float(valor)
    except (ValueError, TypeError):
        return None
    if not math.isfinite(numero):
        return None
    return numero


def validar_registro(registro: dict) -> tuple[bool, list[str]]:
    """Contrato: devuelve (es_valido: bool, motivos: list[str]).
    Valida campos obligatorios, tipos permitidos, formato numérico (compatible con archivos)
    y coherencia de unidades, acumulando todos los motivos encontrados.

    REVISIÓN (A-6): los textos de los motivos empiezan por una etiqueta corta y
    estable («Valor faltante», «Valor no numérico», «Valor fuera de rango»,
    «Unidad no válida», «Tipo no permitido») seguida de ':' y el detalle. La
    interfaz agrupa los motivos por el texto anterior a ':', así que todos los
    registros con el mismo problema quedan en la misma barra del gráfico.
    """
    motivos = []

    if not isinstance(registro, dict):
        return False, ["El registro debe ser un diccionario válido."]

    # TODO A-S10-05: validar campos obligatorios: id, tipo, valor y unidad.
    faltantes = set()
    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in registro or _esta_vacio(registro[campo]):
            faltantes.add(campo)
            motivos.append(f"{campo.capitalize()} faltante: el campo obligatorio '{campo}' no existe o está vacío")

    # REVISIÓN (A-2): antes había un `return` aquí cuando faltaba algún campo.
    # Eso incumplía el TODO A-S10-09 («devolver todos los motivos, no solo el
    # primero»): un registro sin id y con tipo "otro" solo reportaba el id.
    # Ahora se sigue revisando cada campo que SÍ llegó.

    # TODO A-S10-06: validar tipo permitido.
    tipo = registro.get("tipo")
    tipo_conocido = None
    if "tipo" not in faltantes:
        # REVISIÓN (A-2): antes, si el tipo no era texto, se hacía `return` y no
        # se revisaban valor ni unidad. Ahora solo se agrega el motivo.
        # isinstance(tipo, str) va ANTES del `in`: si el tipo fuera una lista,
        # `lista in set` lanzaría TypeError; `and` evalúa en cortocircuito.
        # REVISIÓN (A-8): ya no se quitan tildes aquí; eso lo hace
        # normalizar_registro (antes la misma regla estaba en los dos módulos).
        if isinstance(tipo, str) and tipo in TIPOS_PERMITIDOS:
            tipo_conocido = tipo
        else:
            motivos.append(
                f"Tipo no permitido: '{tipo}' (se esperaba uno de: {', '.join(sorted(TIPOS_PERMITIDOS))})"
            )

    # TODO A-S10-07: validar que valor tenga formato numérico admitido (soporta comas de archivos CSV/Excel).
    numero = None
    if "valor" not in faltantes:
        numero = _a_numero(registro["valor"])
        if numero is None:
            motivos.append(f"Valor no numérico: '{registro['valor']}'")

    # TODO A-S10-08: definir reglas de unidad por tipo de sensor y validación de rangos lógicos.
    unidad = registro.get("unidad")
    # Como en la versión del estudiante, la unidad solo se puede juzgar cuando
    # el tipo es conocido (¿la unidad corresponde a ESE sensor?). Si el tipo no
    # está permitido, el motivo «Tipo no permitido» ya explica el rechazo.
    if "unidad" not in faltantes and tipo_conocido is not None:
        esperada = REGLAS_POR_TIPO[tipo_conocido]["unidad"]
        if unidad != esperada:
            motivos.append(f"Unidad no válida: '{unidad}' para {tipo_conocido} (se esperaba '{esperada}')")

    # Validación de rango numérico lógico (útil para pruebas de calidad)
    if tipo_conocido is not None and numero is not None:
        minimo = REGLAS_POR_TIPO[tipo_conocido]["min"]
        maximo = REGLAS_POR_TIPO[tipo_conocido]["max"]
        if not (minimo <= numero <= maximo):
            motivos.append(
                f"Valor fuera de rango: {numero:g} para {tipo_conocido} (plausible de {minimo:g} a {maximo:g})"
            )

    # TODO A-S10-09: devolver todos los motivos encontrados, no solo el primero.
    es_valido = len(motivos) == 0

    return es_valido, motivos
