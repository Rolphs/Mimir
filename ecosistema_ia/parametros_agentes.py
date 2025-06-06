"""Parámetros configurables para los agentes del ecosistema."""

from dataclasses import dataclass


@dataclass
class ParametrosHerbivoro:
    """Configuración básica para agentes herbívoros."""

    radio_busqueda: int = 2
    umbral_reproduccion: int = 10


@dataclass
class ParametrosCarnivoro:
    """Configuración básica para agentes carnívoros."""

    radio_caza: int = 2
    umbral_reproduccion: int = 20


HERBIVORO = ParametrosHerbivoro()
CARNIVORO = ParametrosCarnivoro()

__all__ = [
    "ParametrosHerbivoro",
    "ParametrosCarnivoro",
    "HERBIVORO",
    "CARNIVORO",
]
