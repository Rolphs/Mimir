from ecosistema_ia.agentes.agente_base import AgenteBase

class DummyA(AgenteBase):
    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="dummy")

    def actuar(self, territorio, otros_agentes=None):
        pass

class DummyB(AgenteBase):
    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="dummy")

    def actuar(self, territorio, otros_agentes=None):
        pass

__all__ = ["DummyA", "DummyB"]
