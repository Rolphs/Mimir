# agente_llm.py

import random
from ecosistema_ia.agentes.tipos.sublimes.sublime_base import SublimeBase


def generar_texto(prompt: str) -> str:
    """Placeholder that simulates an LLM response."""
    ejemplos = [
        "Respuesta generada por LLM",
        "Texto sintetico de ejemplo",
        "Salida ficticia para pruebas"
    ]
    return random.choice(ejemplos)


class AgenteLLM(SublimeBase):
    """Sublime agent that produces text using an LLM (placeholder)."""

    def __init__(self, identificador="LLM-001", x=0, y=0, z=0):
        super().__init__(identificador, x, y, z, funcion="llm")

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        prompt = f"ciclo {self.edad}"
        respuesta = generar_texto(prompt)
        self.excrecion = respuesta
        self.broadcast_mensaje(territorio, respuesta, tipo="llm")
        print(f"🤖 {self.identificador} generó texto: {respuesta}")

    def mutar(self):
        """Cambia la función indicando que es un clon."""
        self.funcion = "llm_mutado"

    def puede_reproducirse(self):
        return self.edad % 2 == 0

    def reproducirse(self, nuevo_id):
        nuevo = AgenteLLM(nuevo_id, self.x, self.y, self.z)
        nuevo.memoria = list(self.memoria[-2:])
        nuevo.mutar()
        print(f"🧬 {self.identificador} clonó a {nuevo.identificador}")
        return nuevo


__all__ = ["AgenteLLM"]
