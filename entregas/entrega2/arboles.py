# Proyecto: SmartRoute Event (Versión 2 - Árboles)
# Integrantes:
# Sergio Andres Martinez Cifuentes 2242039
# Andres Felipe Guaqueta Rojas 2242034
# Andres Sebastian Pinzon Gutierrez 2221887
# Daniel Eduardo Rincon Arias 2202316

"""Sistema de gestión de lugares cercanos usando árboles.

¿Qué hace este programa?
- Guarda lugares (como hoteles o restaurantes) ordenados por distancia
- Permite encontrar rápidamente el lugar más cercano
- Busca lugares por nombre
- Muestra todos los lugares ordenados por distancia

Cada lugar tiene:
- Un nombre (ejemplo: "Hotel Centro")
- La distancia en kilómetros (ejemplo: 1.5)
- El tiempo estimado (ejemplo: "10 min caminando")
- Un tipo (ejemplo: "Hotel", "Restaurante", etc.)

Los lugares se organizan en un árbol donde:
- A la izquierda van los más cercanos
- A la derecha los más lejanos
"""

from typing import Optional, List, Tuple


# Clase Nodo: representa cada lugar en el árbol

class Nodo:
    """Nodo del árbol que representa un lugar.

    Cada lugar guarda:
    - nombre: el nombre del lugar (ejemplo: "Hotel Centro")
    - distancia: qué tan lejos está en km (ejemplo: 1.5)
    - tiempo: cuánto tarda llegar (ejemplo: "10 min caminando")
    - tipo: qué tipo de lugar es (ejemplo: "Hotel")
    - izq, der: conexión a otros lugares (más cercanos a la izquierda, más lejanos a la derecha)
    """

    def __init__(self, nombre: str, distancia: float, tiempo: str, tipo: str):
        self.nombre: str = nombre
        self.distancia: float = distancia
        self.tiempo: str = tiempo
        self.tipo: str = tipo
        self.izq: Optional["Nodo"] = None
        self.der: Optional["Nodo"] = None

    def __repr__(self) -> str:
        # Representación útil para debugging
        return f"Nodo({self.nombre!r}, {self.distancia} km, {self.tiempo!r}, {self.tipo!r})"



# Clase ArbolLugares: administra los lugares y sus relaciones

class ArbolLugares:
    """Organiza los lugares para encontrarlos fácilmente.

    Esta clase guarda todos los lugares de forma ordenada por distancia,
    así podemos:
    - Encontrar rápido el lugar más cercano
    - Ver todos los lugares ordenados del más cercano al más lejano
    - Buscar un lugar por su nombre
    """

    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None

    def insertar(self, nombre: str, distancia: float, tiempo: str, tipo: str) -> None:
        """Inserta un nuevo lugar en el árbol.

        Para agregar un lugar necesitas:
        - nombre: cómo se llama el lugar
        - distancia: a cuántos km está
        - tiempo: cuánto se tarda en llegar
        - tipo: qué tipo de lugar es

        Nota: Si dos lugares están a la misma distancia, el nuevo
        se guarda a la derecha del que ya estaba.
        """

        # Aseguramos que distancia sea numérica para evitar comparaciones
        # inesperadas en tiempo de ejecución.
        try:
            distancia_val = float(distancia)
        except (TypeError, ValueError):
            raise ValueError("distancia debe ser un número (float o int)")

        nuevo = Nodo(nombre, distancia_val, tiempo, tipo)
        if not self.raiz:
            self.raiz = nuevo
        else:
            self._insertar(self.raiz, nuevo)

    def _insertar(self, actual: Nodo, nuevo: Nodo) -> None:
        """Inserta recursivamente `nuevo` a partir del nodo `actual`.

        Si la distancia de `nuevo` es menor que la de `actual` se va a
        la rama izquierda, en caso contrario se va a la derecha.
        """

        if nuevo.distancia < actual.distancia:
            if actual.izq:
                self._insertar(actual.izq, nuevo)
            else:
                actual.izq = nuevo
        else:
            if actual.der:
                self._insertar(actual.der, nuevo)
            else:
                actual.der = nuevo

    def inorden(self) -> List[Tuple[str, float, str, str]]:
        """Muestra todos los lugares ordenados por distancia.
        
        Imprime cada lugar con su información y devuelve una lista
        con todos los lugares, empezando por el más cercano.
        """

        resultados: List[Tuple[str, float, str, str]] = []

        def recorrer(nodo: Optional[Nodo]) -> None:
            if nodo:
                recorrer(nodo.izq)
                # Imprimimos para mantener el comportamiento original
                print(f"{nodo.tipo}: {nodo.nombre} – {nodo.distancia} km ({nodo.tiempo})")
                resultados.append((nodo.tipo, nodo.nombre, nodo.distancia, nodo.tiempo))
                recorrer(nodo.der)

        if not self.raiz:
            print("No hay lugares registrados.")
        else:
            recorrer(self.raiz)

        return resultados

    def buscar(self, nombre: str) -> Optional[Nodo]:
        """Busca un lugar por su nombre.
        
        Escribe el nombre del lugar y te dice:
        - Si lo encontró o no
        - Si existe, muestra su distancia y tiempo
        """

        def _buscar(nodo: Optional[Nodo]) -> Optional[Nodo]:
            if not nodo:
                return None
            if nodo.nombre.lower() == nombre.lower():
                return nodo
            izq = _buscar(nodo.izq)
            if izq:
                return izq
            return _buscar(nodo.der)

        resultado = _buscar(self.raiz)
        if resultado:
            print(f"Encontrado: {resultado.nombre} – {resultado.distancia} km ({resultado.tiempo})")
        else:
            print("No encontrado.")

        return resultado

    def buscar_mas_cercano(self) -> Optional[Nodo]:
        """Encuentra el lugar más cercano de todos.
        
        Busca y muestra el lugar que está a menor distancia
        de todos los guardados.
        """

        actual = self.raiz
        if not actual:
            print("No hay lugares registrados.")
            return None
        while actual.izq:
            actual = actual.izq
        print(f"El lugar más cercano es: {actual.nombre} – {actual.distancia} km ({actual.tiempo})")
        return actual



# Ejemplo de uso del programa

if __name__ == "__main__":
    arbol = ArbolLugares()

    # Agregamos lugares de prueba
    arbol.insertar("Clínica Central Norte", 1.8, "6 min en carro", "Emergencia")
    arbol.insertar("Hotel Mirador del Sol", 1.2, "15 min caminando", "Hotel")
    arbol.insertar("Panadería La Delicia", 0.8, "10 min caminando", "Snack")
    arbol.insertar("Restaurante El Sabor Local", 2.4, "8 min caminando", "Restaurante")

    print("\n--- Lugares registrados (ordenados por distancia) ---")
    arbol.inorden()

    print("\nBuscando 'Hotel Mirador del Sol'...")
    arbol.buscar("Hotel Mirador del Sol")

    print("\nBuscando 'Parque Central'...")
    arbol.buscar("Parque Central")

    print("\nBuscando lugar más cercano...")
    arbol.buscar_mas_cercano()
