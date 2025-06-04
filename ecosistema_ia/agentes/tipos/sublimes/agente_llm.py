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
        territorio.buzon_mensajes.append({
            "emisor": self.identificador,
            "tipo": "llm",
            "mensaje": respuesta,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        })
        print(f"🤖 {self.identificador} generó texto: {respuesta}")


__all__ = ["AgenteLLM"]
