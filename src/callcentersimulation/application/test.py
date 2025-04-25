import multiprocessing
from typing import List


class ListaConcurrente:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.lista = self.manager.list()
        self.lock = multiprocessing.Lock()

    def agregar_elemento(self, valor: str) -> None:
        with self.lock:
            self.lista.append(valor)

    def obtener_lista(self) -> List[str]:
        with self.lock:
            return list(self.lista)


def worker(lista: ListaConcurrente, id_proceso: int) -> None:
    for i in range(3):
        nuevo_elemento = f"Proceso-{id_proceso}-Iter-{i}"
        lista.agregar_elemento(nuevo_elemento)


def main():
    lista_compartida = ListaConcurrente()
    procesos = []

    try:
        num_procesos = int(input("Ingrese número de procesos: "))
    except ValueError:
        print("Entrada inválida. Usando valor por defecto (4)")
        num_procesos = 4

    for i in range(num_procesos):
        p = multiprocessing.Process(
            target=worker,
            args=(lista_compartida, i)
        )
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("\nResultado final (paralelismo real):")
    print('\n'.join(lista_compartida.obtener_lista()))


if __name__ == "__main__":
    main()
