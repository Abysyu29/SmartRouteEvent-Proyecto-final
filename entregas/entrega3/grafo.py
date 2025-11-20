# Proyecto: SmartRoute Event (Versión 3 - Grafos)
# Integrantes:
# Sergio Andres Martinez Cifuentes 2242039
# Andres Felipe Guaqueta Rojas 2242034
# Andres Sebastian Pinzon Gutierrez 2221887
# Daniel Eduardo Rincon Arias 2202316

"""
Implementación de un grafo para gestionar lugares cercanos.

Contiene la estructura de datos de GRAFO que permite tratar las
relaciones entre lugares (nodos) y las distancias/conexiones entre ellos (aristas).
"""

from typing import Dict, Any, List, Tuple, Optional
import heapq

# CLASE: NODO

class Nodo:
    """
    Representa un lugar o punto de interés.
    
    Cada nodo contiene información detallada sobre un lugar, como su nombre,
    ubicación (distancia), tiempo de viaje y categoría (hotel, restaurante, etc.).
    """
    
    def __init__(self, node_id: str, nombre: str, distancia_km: float,
                    categoria: str, meta: Optional[Dict[str,Any]]=None):
        """
        Inicializa un nodo con sus atributos principales.
        
        Parámetros:
            node_id (str): Identificador único del nodo (ej: "P1", "H1")
            nombre (str): Nombre del lugar (ej: "Panadería La Delicia")
            distancia_km (float): Distancia desde el punto de referencia en km
            categoria (str): Tipo de lugar (Hotel, Restaurante, Snack, Emergencia, etc.)
            meta (dict, opcional): Diccionario con información adicional del lugar
        """
        self.id = node_id
        self.nombre = nombre
        self.distancia_km = distancia_km
        self.categoria = categoria
        self.meta = meta or {}

    def to_dict(self):
        """
        Convierte el nodo a un diccionario para fácil acceso.
        
        Retorna:
            dict: Información del nodo en formato diccionario
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "distancia_km": self.distancia_km,
            "categoria": self.categoria,
            **self.meta  # Incluye metadatos adicionales si existen
        }

    def __repr__(self):
        """
        Representación en texto del nodo (usada para impresión y debugging).
        
        Retorna:
            str: Formato legible del nodo (ej: "Nodo(P1, Panadería La Delicia, Snack)")
        """
        return f"Nodo({self.id}, {self.nombre}, {self.categoria})"



# CLASE: GRAFO

class Grafo:
    """
    Estructura de datos que representa un grafo (red de nodos conectados).
    Permite gestionar lugares (nodos) y las conexiones/distancias entre ellos (aristas).
    
    Ejemplo de uso:
        g = Grafo(dirigido=False)
        g.insertar_nodo(Nodo("P1", "Panadería", 0.8, "Snack"))
        g.insertar_arista("P1", "R1", peso=0.6)
    """
    
    def __init__(self, dirigido: bool=False):
        """
        Inicializa un grafo vacío.
        
        Parámetros:
            dirigido (bool): Si True, las aristas tienen dirección (A->B es diferente a B->A)
                           Si False, las conexiones son bidireccionales
        """
        self.dirigido = dirigido
        self.nodos: Dict[str, Nodo] = {}  # Diccionario: id_nodo -> objeto Nodo
        self.ady: Dict[str, List[Tuple[str, float, Dict[str,Any]]]] = {}  # Lista de adyacencia

    def insertar_nodo(self, nodo: Nodo):
        """
        Añade un nuevo nodo (lugar) al grafo.
        
        Parámetros:
            nodo (Nodo): El nodo a insertar
            
        Lanza:
            ValueError: Si ya existe un nodo con ese id
        """
        if nodo.id in self.nodos:
            raise ValueError(f"Ya existe un nodo con id {nodo.id}")
        self.nodos[nodo.id] = nodo  # Guardar el nodo
        self.ady[nodo.id] = []  # Inicializar lista de adyacencia vacía

    def eliminar_nodo(self, node_id: str):
        """
        Elimina un nodo del grafo junto con todas sus conexiones.
        
        Parámetros:
            node_id (str): ID del nodo a eliminar
            
        Lanza:
            KeyError: Si el nodo no existe
        """
        if node_id not in self.nodos:
            raise KeyError(f"No existe el nodo {node_id}")
        
        # Eliminar todas las aristas que apunten a este nodo
        for u, lst in list(self.ady.items()):
            self.ady[u] = [t for t in lst if t[0] != node_id]
        
        # Eliminar el nodo y sus adyacencias
        del self.ady[node_id]
        del self.nodos[node_id]

    def buscar_nodo_por_id(self, node_id: str):
        """
        Busca un nodo por su identificador único.
        
        Parámetros:
            node_id (str): ID del nodo a buscar
            
        Retorna:
            Nodo o None: El nodo si existe, None en caso contrario
        """
        return self.nodos.get(node_id)

    def buscar_nodo_por_nombre(self, nombre: str):
        """
        Busca nodos por nombre (búsqueda insensible a mayúsculas).
        
        Parámetros:
            nombre (str): Nombre del lugar a buscar
            
        Retorna:
            list: Lista de nodos que coinciden con el nombre
        """
        return [n for n in self.nodos.values() if n.nombre.lower() == nombre.lower()]

    def buscar_por_categoria(self, categoria: str):
        """
        Busca todos los nodos de una categoría específica.
        
        Parámetros:
            categoria (str): Tipo de lugar (ej: "Hotel", "Restaurante")
            
        Retorna:
            list: Todos los nodos de esa categoría
        """
        return [n for n in self.nodos.values() if n.categoria.lower() == categoria.lower()]

    def insertar_arista(self, u: str, v: str, peso: float=1.0, meta=None):
        """
        Crea una conexión (arista) entre dos nodos.
        
        Parámetros:
            u (str): ID del nodo origen
            v (str): ID del nodo destino
            peso (float): Distancia/costo de la conexión (por defecto 1.0)
            meta (dict, opcional): Información adicional sobre la conexión
            
        Lanza:
            KeyError: Si alguno de los nodos no existe
            
        Nota: Si el grafo no es dirigido, la conexión se crea en ambas direcciones.
        """
        if u not in self.nodos or v not in self.nodos:
            raise KeyError("Ambos nodos deben existir para insertar una arista")
        
        # Agregar arista u -> v
        self.ady[u].append((v, peso, meta or {}))
        
        # Si no es dirigido, agregar también v -> u
        if not self.dirigido:
            self.ady[v].append((u, peso, meta or {}))

    def eliminar_arista(self, u: str, v: str, eliminar_todas: bool=False):
        """
        Elimina la(s) conexión(es) entre dos nodos.
        
        Parámetros:
            u (str): ID del nodo origen
            v (str): ID del nodo destino
            eliminar_todas (bool): Si True, elimina todos los pesos que conectan u->v
                                  Si False, elimina solo la primera
        """
        if u not in self.ady:
            return
        
        # Eliminar de u -> v
        if eliminar_todas:
            self.ady[u] = [t for t in self.ady[u] if t[0] != v]
        else:
            for i, t in enumerate(self.ady[u]):
                if t[0] == v:
                    del self.ady[u][i]
                    break
        
        # Si no es dirigido, eliminar también de v -> u
        if not self.dirigido:
            if v in self.ady:
                if eliminar_todas:
                    self.ady[v] = [t for t in self.ady[v] if t[0] != u]
                else:
                    for i, t in enumerate(self.ady[v]):
                        if t[0] == u:
                            del self.ady[v][i]
                            break

    def bfs(self, inicio_id: str):
        """
        Búsqueda por Amplitud (BFS - Breadth-First Search).
        
        Recorre el grafo nivel por nivel, comenzando desde un nodo.
        Útil para encontrar el camino más corto en grafos sin pesos.
        
        Parámetros:
            inicio_id (str): ID del nodo inicial
            
        Retorna:
            list: Orden de los nodos visitados
            
        Lanza:
            KeyError: Si el nodo inicio no existe
        """
        if inicio_id not in self.nodos:
            raise KeyError("Nodo inicio no existe")
        
        visitados = set([inicio_id])
        cola = [inicio_id]
        orden = []
        
        while cola:
            u = cola.pop(0)  # Tomar el primer elemento (FIFO)
            orden.append(u)
            
            # Explorar todos los vecinos
            for v, *_ in self.ady.get(u, []):
                if v not in visitados:
                    visitados.add(v)
                    cola.append(v)
        
        return orden

    def dfs(self, inicio_id: str):
        """
        Búsqueda por Profundidad (DFS - Depth-First Search).
        
        Recorre el grafo explorando en profundidad antes de pasar al siguiente vecino.
        Útil para detectar ciclos y componentes conectadas.
        
        Parámetros:
            inicio_id (str): ID del nodo inicial
            
        Retorna:
            list: Orden de los nodos visitados
            
        Lanza:
            KeyError: Si el nodo inicio no existe
        """
        if inicio_id not in self.nodos:
            raise KeyError("Nodo inicio no existe")
        
        visitados = set()
        orden = []
        
        def _dfs(u):
            """Función recursiva para DFS"""
            visitados.add(u)
            orden.append(u)
            
            # Explorar recursivamente todos los vecinos no visitados
            for v, *_ in self.ady.get(u, []):
                if v not in visitados:
                    _dfs(v)
        
        _dfs(inicio_id)
        return orden

    def dijkstra(self, inicio_id: str, objetivo_id=None):
        """
        Algoritmo de Dijkstra para encontrar caminos más cortos.
        
        Calcula la distancia mínima desde el nodo inicio a todos los otros nodos.
        Utiliza una cola de prioridad (heap) para eficiencia.
        
        Parámetros:
            inicio_id (str): ID del nodo inicial
            objetivo_id (str, opcional): Si se especifica, detiene al alcanzar este nodo
            
        Retorna:
            tuple: (distancias, predecesores)
                - distancias: dict con la distancia mínima a cada nodo
                - predecesores: dict con el nodo previo en el camino óptimo
                
        Lanza:
            KeyError: Si el nodo inicio no existe
        """
        if inicio_id not in self.nodos:
            raise KeyError("Nodo inicio no existe")
        
        # Inicializar distancias como infinito, excepto el nodo inicio
        dist = {node_id: float('inf') for node_id in self.nodos}
        prev = {node_id: None for node_id in self.nodos}
        dist[inicio_id] = 0.0
        
        heap = [(0.0, inicio_id)]  # (distancia, nodo)
        
        while heap:
            d, u = heapq.heappop(heap)  # Tomar nodo con menor distancia
            
            # Si ya encontramos una distancia mejor, saltar
            if d > dist[u]:
                continue
            
            # Si encontramos el objetivo, podemos detener
            if objetivo_id is not None and u == objetivo_id:
                break
            
            # Relajar aristas: intentar mejorar distancias a vecinos
            for v, peso, _meta in self.ady.get(u, []):
                nd = d + peso
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        
        return dist, prev

    def reconstruir_camino(self, prev, objetivo_id):
        """
        Reconstruye el camino óptimo usando los predecesores de Dijkstra.
        
        Parámetros:
            prev (dict): Diccionario de predecesores (salida de dijkstra)
            objetivo_id (str): Nodo destino
            
        Retorna:
            list: Secuencia de nodos desde el origen hasta el objetivo
        """
        camino = []
        u = objetivo_id
        
        # Seguir los predecesores hacia atrás hasta el origen
        while u is not None:
            camino.append(u)
            u = prev[u]
        
        camino.reverse()  # Invertir para obtener el orden correcto
        return camino

    def listar_nodos(self):
        """
        Obtiene información de todos los nodos en formato diccionario.
        
        Retorna:
            list: Lista de diccionarios con la información de cada nodo
        """
        return [n.to_dict() for n in self.nodos.values()]

    def listar_adyacencias(self):
        """
        Obtiene la lista de adyacencia completa del grafo.
        
        Retorna:
            dict: Estructura {nodo_origen: [(nodo_destino, peso, metadatos), ...], ...}
        """
        return self.ady
