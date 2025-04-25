import multiprocessing
import random
import time
from typing import List
from datetime import datetime

animales = sorted(["perro", "gato", "elefante", "jirafa", "tigre",
                   "leon", "zorro", "conejo", "lobo", "oso"])


class ListaConcurrente:
    def __init__(self, manager: multiprocessing.Manager):
        self.lista = manager.list(animales)
        self.lock = manager.Lock()
        self.print_lock = manager.Lock()
        self.start_time = time.perf_counter()
        self.cola = manager.Queue()
        self._inicializar_cola()

    def _inicializar_cola(self):
        for elemento in self.lista:
            self.cola.put(elemento)

    def obtener_elemento(self):
        try:
            return self.cola.get_nowait()
        except:
            return None

    def modificar_elemento(self, original: str, modificado: str) -> None:
        with self.lock:
            indice = self.lista.index(original)
            self.lista[indice] = modificado

    def log(self, mensaje: str) -> None:
        with self.print_lock:
            tiempo_transcurrido = time.perf_counter() - self.start_time
            print(f"[+{tiempo_transcurrido:6.2f}s] {mensaje}", flush=True)


def worker(lista: ListaConcurrente, id_proceso: int) -> None:
    while True:
        elemento = lista.obtener_elemento()
        if elemento is None:
            break

        # Simulación de procesamiento
        tiempo_espera = random.uniform(0, 4)
        time.sleep(tiempo_espera)

        # Modificación del elemento
        elemento_modificado = elemento.upper()
        lista.modificar_elemento(elemento, elemento_modificado)

        # Log detallado
        lista.log(
            f"PID-{id_proceso} | "
            f"Procesó: {elemento} → {elemento_modificado} | "
            f"Espera: {tiempo_espera:.2f}s"
        )


def main():
    with multiprocessing.Manager() as manager:
        lista_compartida = ListaConcurrente(manager)
        procesos = []

        try:
            num_procesos = int(input("Ingrese número de procesos: "))
        except ValueError:
            num_procesos = 4
            print(f"Usando {num_procesos} procesos por defecto")

        lista_compartida.log("🚀 INICIO - Lista original ordenada:")
        lista_compartida.log('\n'.join(lista_compartida.lista))
        lista_compartida.log("\n⚡ Iniciando procesamiento paralelo:\n")

        for i in range(num_procesos):
            p = multiprocessing.Process(
                target=worker,
                args=(lista_compartida, i)
            )
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()

        lista_compartida.log("\n✅ PROCESO COMPLETADO - Lista final:")
        lista_compartida.log('\n'.join(lista_compartida.lista))


if __name__ == "__main__":
    main()
