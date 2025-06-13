"""Core base class for all Mimir agents."""

from collections import deque

class AgenteBase:
    """Base behaviour shared by herbivores, carnivores and sublime agents."""

    def __init__(self, identificador, x, y, z, funcion="agente", memoria_max=100, memoria_vida=None):
        self.identificador = identificador
        self.x = x
        self.y = y
        self.z = z
        self.funcion = funcion

        self.edad = 0
        self.memoria = []
        self.memoria_max = memoria_max
        self.memoria_vida = memoria_vida
        self.recompensa_total = 0
        self.alianzas = set()

        self.calificacion = None
        self.alimentacion = None
        self.excrecion = None

        self.mensajeria = deque(maxlen=10)
        self.modelo_ml = None
        self.X_train = []
        self.y_train = []
        self.entrenado = False

    def __repr__(self):
        return f"{self.funcion.capitalize()}({self.identificador} at {self.x},{self.y},{self.z})"

    @property
    def posicion(self):
        return (self.x, self.y, self.z)

    def incrementar_edad(self):
        self.edad += 1
        self.prune_memoria()

    def puede_reproducirse(self):
        return False

    def reproducirse(self, nuevo_id):
        raise NotImplementedError("Este agente no tiene lógica de reproducción definida.")

    def actuar(self, territorio, otros_agentes=None):
        raise NotImplementedError("Este agente no tiene comportamiento definido.")

    def log_memoria(self, entrada, resultado, exitoso=False):
        self.memoria.append({
            "edad": self.edad,
            "entrada": entrada,
            "resultado": resultado,
            "exitoso": exitoso
        })
        self.prune_memoria()

    def prune_memoria(self):
        """Remove stale entries from memory based on age and size limits."""
        if self.memoria_vida is not None:
            self.memoria = [m for m in self.memoria if self.edad - m.get("edad", self.edad) < self.memoria_vida]
        if len(self.memoria) > self.memoria_max:
            self.memoria = self.memoria[-self.memoria_max:]

    def enviar_mensaje(self, mensaje, receptor):
        """Deliver a direct message to another agent."""
        receptor.recibir_mensaje((self.identificador, mensaje))

    def recibir_mensaje(self, mensaje):
        self.mensajeria.append(mensaje)

    def broadcast_mensaje(self, territorio, contenido, tipo="informacion"):
        """Append a message to the shared territory mailbox."""
        territorio.buzon_mensajes.append({
            "emisor": self.identificador,
            "funcion": self.funcion,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "dato_util": contenido,
            "tipo": tipo,
            "ciclo": self.edad,
        })

    def mover(self, dx=0, dy=0, dz=0, territorio=None):
        """Move the agent while keeping coordinates within the territory."""
        self.x += dx
        self.y += dy
        self.z += dz
        if territorio:
            self.z = max(0, min(self.z, len(territorio.csvs) - 1))
            datos = territorio.get_csv(self.z)
            if datos:
                self.x = max(0, min(self.x, len(datos) - 1))
                fila_len = len(datos[self.x]) if 0 <= self.x < len(datos) else 0
                self.y = max(0, min(self.y, fila_len - 1 if fila_len else 0))
            else:
                self.x = max(0, self.x)
                self.y = max(0, self.y)

    def describir(self):
        return {
            "id": self.identificador,
            "funcion": self.funcion,
            "posicion": self.posicion,
            "edad": self.edad,
            "recompensa_total": self.recompensa_total,
            "memoria_len": len(self.memoria),
            "alianzas": list(self.alianzas),
            "calificacion": self.calificacion
        }

    # ML
    def inicializar_modelo(self, modelo):
        self.modelo_ml = modelo

    def entrenar_modelo(self):
        if self.modelo_ml and len(self.X_train) >= 5:
            clases = set(self.y_train)
            if len(clases) < 2:
                opuesta = 0 if list(clases)[0] == 1 else 1
                self.X_train.append([0, 0, 0])
                self.y_train.append(opuesta)
                print(f"🧠 {self.identificador} insertó muestra sintética para entrenar.")
            self.modelo_ml.fit(self.X_train, self.y_train)
            self.entrenado = True

    def reforzar_modelo(self, features, etiqueta):
        self.X_train.append(features)
        self.y_train.append(1 if etiqueta else 0)
        self.entrenar_modelo()


__all__ = ["AgenteBase"]
