import threading
import time

class ResponseWaiter:
    def __init__(self, timeout=5):
        self._eventos = {}
        self._lock = threading.Lock()
        self._timeout = timeout

    def _clave(self, cliente_id, accion):
        return f"{cliente_id}:{accion}"

    def esperar_respuesta(self, cliente_id, accion):
        clave = self._clave(cliente_id, accion)
        evento = threading.Event()
        with self._lock:
            self._eventos[clave] = evento

        recibido = evento.wait(timeout=self._timeout)

        with self._lock:
            self._eventos.pop(clave, None)

        return recibido

    def notificar_respuesta(self, cliente_id, accion):
        clave = self._clave(cliente_id, accion)
        with self._lock:
            evento = self._eventos.get(clave)
            if evento:
                evento.set()
