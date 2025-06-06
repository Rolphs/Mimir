"""Funciones de apoyo para interacciones entre agentes."""

from __future__ import annotations

from math import sqrt
from typing import Iterable, List


def distancia_euclidiana(a, b) -> float:
    """Calcular distancia euclidiana entre dos agentes."""
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def agentes_en_rango(agente, agentes: Iterable, radio: int = 2) -> List:
    """Devuelve una lista de agentes dentro de un radio dado."""
    cercanos = []
    for otro in agentes:
        if otro is agente:
            continue
        if distancia_euclidiana(agente, otro) <= radio:
            cercanos.append(otro)
    return cercanos


def registrar_interaccion(emisor, receptor, recompensa: int = 1) -> None:
    """Actualizar contadores básicos tras una interacción."""
    emisor.interacciones = getattr(emisor, "interacciones", 0) + 1
    receptor.interacciones = getattr(receptor, "interacciones", 0) + 1
    emisor.recompensa_total = getattr(emisor, "recompensa_total", 0) + recompensa
