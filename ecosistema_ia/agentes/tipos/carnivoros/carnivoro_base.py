# carnivoro_base.py

from agentes.agente_base import AgenteBase

class CarnivoroBase(AgenteBase):
    def __init__(self, identificador, x, y, z, funcion="carnivoro"):
        super().__init__(identificador, x, y, z, funcion=funcion)
        self.objetivo_actual = None
        self.interacciones = 0
        self.recompensa_total = 0

    def buscar_objetivo(self, agentes):
        """Busca agentes cercanos con los que pueda interactuar"""
        candidatos = [
            a for a in agentes
            if a.identificador != self.identificador and abs(a.x - self.x) <= 2 and abs(a.y - self.y) <= 2 and a.z == self.z
        ]
        if candidatos:
            self.objetivo_actual = candidatos[0]
        else:
            self.objetivo_actual = None
        return self.objetivo_actual

    def evaluar_objetivo(self, agente):
        """Regla abstracta: cada carnívoro definirá si el objetivo es válido"""
        raise NotImplementedError("Cada subclase debe definir cómo evalúa a su objetivo")

    def actuar(self, territorio, otros_agentes=None):
        """Acción base: buscar objetivo y decidir si se interactúa"""
        self.incrementar_edad()
        if not otros_agentes:
            return

        objetivo = self.buscar_objetivo(otros_agentes)
        if objetivo and self.evaluar_objetivo(objetivo):
            self.interactuar(objetivo, territorio)
        else:
            self.log_memoria(
                entrada="Sin objetivo válido",
                resultado="Esperando oportunidad",
                exitoso=False
            )

    def interactuar(self, objetivo, territorio):
        """Interacción base, que puede ser sobrescrita (absorber, dividir, destruir...)"""
        raise NotImplementedError("La interacción debe ser implementada por la subclase")

    def puede_reproducirse(self):
        return False

    def reproducirse(self, nuevo_id):
        raise NotImplementedError("Este carnívoro no define su lógica de reproducción")

__all__ = ["CarnivoroBase"]