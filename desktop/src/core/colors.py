"""Tokens de color de la identidad visual de VecinoSeguro.

Estos valores se obtienen directamente de la Guía de Imagen Corporativa UI
(Mayo 2026). Todo componente, vista o widget debe consumir estos tokens
en lugar de literales en hexadecimal, lo que garantiza coherencia visual
entre desktop, móvil y futuras piezas del sistema.

Su uso facilita además realizar cambios globales de identidad si en el
futuro se decide ajustar la paleta corporativa.
"""


class Colors:
    """Paleta principal y funcional de VecinoSeguro."""

    # ---- Paleta principal ----
    PRIMARY = "#005A9C"        # Azul principal: acciones, navegación, encabezados
    SUCCESS = "#22A63A"        # Verde principal: confirmaciones, estados positivos
    DARK_PRIMARY = "#073B6B"   # Azul oscuro: texto fuerte, sidebar, fondos altos
    DARK_SUCCESS = "#16812C"   # Verde oscuro: variantes secundarias y estados confirmados
    SURFACE = "#F4F8FB"        # Fondo general claro
    WHITE = "#FFFFFF"          # Tarjetas, formularios, modales

    # ---- Paleta funcional / semántica ----
    INFO = "#2F80ED"           # Información, estados intermedios
    WARNING = "#F2A900"        # Advertencia, urgencia media
    DANGER = "#D92D20"         # Crítico, peligro, urgencia alta
    TEXT = "#102A43"           # Texto principal: títulos, contenido relevante
    TEXT_SECONDARY = "#52616B" # Texto secundario: metadatos, fechas
    BORDER = "#D9E2EC"         # Bordes suaves, separadores

    # ---- Variantes de fondo para badges (derivadas) ----
    BG_SUCCESS = "#E5F4EA"
    BG_INFO = "#E5F0FB"
    BG_WARNING = "#FFF4E5"
    BG_DANGER = "#FED7D7"
    BG_NEUTRAL = "#E2E8F0"

    # ---- Tonos auxiliares para sidebar y elementos sobre fondo oscuro ----
    SIDEBAR_TEXT = "#C8D4E5"
    SIDEBAR_SECTION = "#6B85A8"


class Typography:
    """Familias tipográficas recomendadas por la guía visual."""

    # Inter es la fuente recomendada; las alternativas garantizan
    # compatibilidad si el sistema no la tiene instalada.
    FAMILY = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"

    SIZE_H1 = 26
    SIZE_H2 = 18
    SIZE_H3 = 15
    SIZE_BODY = 13
    SIZE_SMALL = 12
    SIZE_MICRO = 11
