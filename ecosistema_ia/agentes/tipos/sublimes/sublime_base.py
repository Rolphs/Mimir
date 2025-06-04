"""Base class for sublime agents."""

from ecosistema_ia.agentes.agente_base import AgenteBase


class SublimeBase(AgenteBase):
    """Minimal base class for high-level "sublime" agents."""

    def __init__(self, identificador, x, y, z, funcion="sublime"):
        super().__init__(identificador, x, y, z, funcion=funcion)


__all__ = ["SublimeBase"]


