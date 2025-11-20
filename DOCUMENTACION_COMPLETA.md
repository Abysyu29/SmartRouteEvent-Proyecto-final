# DOCUMENTACIÓN COMPLETA: SmartRoute Event - Grafos
# Proyecto: SmartRoute Event (Versión 3 - Grafos)

# Integrantes:
# Sergio Andres Martinez Cifuentes 2242039
# Andres Felipe Guaqueta Rojas 2242034
# Andres Sebastian Pinzon Gutierrez 2221887
# Daniel Eduardo Rincon Arias 2202316

## Explicación del Flujo y Conexión entre `grafo.py` y `ejemplo.py`

---

##  TABLA DE CONTENIDOS

1. [Descripción General](#descripción-general)
2. [Estructura de `grafo.py`](#estructura-de-grafopy)
3. [Estructura de `ejemplo.py`](#estructura-de-ejemplopy)
4. [Flujo de Ejecución](#flujo-de-ejecución)
5. [Conceptos Teóricos](#conceptos-teóricos)
6. [Ejemplos de Uso](#ejemplos-de-uso)

---

## DESCRIPCIÓN GENERAL

Este proyecto implementa un **sistema de gestión de lugares cercanos** usando estructuras de datos de **grafos**. 

**Objetivo:** Encontrar rutas óptimas y eficientes entre diferentes lugares en una ciudad.

**Casos de uso:**
- Sistema de búsqueda de hoteles, restaurantes, clínicas cercanas
- Cálculo de caminos más cortos entre ubicaciones
- Análisis de conectividad entre puntos de interés

---

## ESTRUCTURA DE `grafo.py`

###  CLASE NODO

```python
class Nodo:
    """Representa un lugar o punto de interés"""
    def __init__(self, node_id, nombre, distancia_km, categoria, meta=None):
```

**Propósito:** Almacenar información de un lugar individual.

**Atributos:**
- `id`: Identificador único (ej: "P1", "H1")
- `nombre`: Nombre del lugar (ej: "Panadería La Delicia")
- `distancia_km`: Distancia desde referencia (ej: 0.8 km)
- `categoria`: Tipo de lugar (Hotel, Restaurante, Snack, Emergencia)
- `meta`: Diccionario para información adicional

**Métodos principales:**
- `to_dict()`: Convierte el nodo a diccionario para fácil acceso
- `__repr__()`: Representación en texto para debugging

**Ejemplo:**
```python
nodo = Nodo("P1", "Panadería La Delicia", 0.8, "Snack")
print(nodo)  # Salida: Nodo(P1, Panadería La Delicia, Snack)
```

---

###  CLASE GRAFO

```python
class Grafo:
    """Estructura de datos que conecta nodos mediante aristas"""
    def __init__(self, dirigido=False):
```

**Propósito:** Almacenar y gestionar una red de lugares y sus conexiones.

**Atributos internos:**
- `dirigido`: Booleano (True = sentido único, False = bidireccional)
- `nodos`: Diccionario {id_nodo: objeto_Nodo}
- `ady`: Lista de adyacencia {nodo_origen: [(destino, peso, metadatos), ...]}

---

###  MÉTODOS DE GESTIÓN DE NODOS

#### `insertar_nodo(nodo)`
Agrega un nuevo lugar al sistema.
```python
grafo.insertar_nodo(Nodo("P1", "Panadería", 0.8, "Snack"))
# Resultado: El nodo "P1" se almacena y está disponible para conexiones
```

#### `eliminar_nodo(node_id)`
Elimina un lugar y todas sus conexiones.
```python
grafo.eliminar_nodo("P1")
# Resultado: "P1" se elimina, y cualquier arista conectada se borra también
```

#### `buscar_nodo_por_id(node_id)`
Busca rápidamente un lugar por su identificador.
```python
nodo = grafo.buscar_nodo_por_id("P1")
# Retorna el objeto Nodo si existe, None si no
```

#### `buscar_nodo_por_nombre(nombre)`
Busca lugares por nombre (insensible a mayúsculas).
```python
hoteles = grafo.buscar_nodo_por_nombre("Hotel")
# Retorna lista de nodos que coinciden con ese nombre
```

#### `buscar_por_categoria(categoria)`
Encuentra todos los lugares de un tipo específico.
```python
restaurantes = grafo.buscar_por_categoria("Restaurante")
# Retorna lista de todos los restaurantes
```

---

###  MÉTODOS DE GESTIÓN DE CONEXIONES (ARISTAS)

#### `insertar_arista(u, v, peso=1.0, meta=None)`
Crea una conexión entre dos lugares.
```python
grafo.insertar_arista("P1", "R1", peso=0.6)
# Crea un camino de 0.6 km entre Panadería y Restaurante
# Si el grafo no es dirigido, crea la conexión en ambas direcciones
```

#### `eliminar_arista(u, v, eliminar_todas=False)`
Rompe una conexión entre lugares.
```python
grafo.eliminar_arista("P1", "R1")
# Elimina la conexión entre Panadería y Restaurante
```

#### `listar_adyacencias()`
Obtiene todas las conexiones del grafo.
```python
adyacencias = grafo.listar_adyacencias()
# Retorna: {"P1": [("R1", 0.6, {}), ("H1", 0.5, {})], ...}
```

---

###  MÉTODOS DE BÚSQUEDA Y ALGORITMOS

#### `bfs(inicio_id)` - Búsqueda por Amplitud
Explora todos los nodos nivel por nivel desde un inicio.

**¿Cuándo usarlo?**
- Encontrar nodos a distancia mínima (en términos de número de saltos)
- Exploración rápida de la vecindad

**Ejemplo:**
```python
orden = grafo.bfs("P1")
# Resultado: ["P1", "R1", "H1", "C1"]
# Primero visita P1, luego sus vecinos (R1, H1), luego sus vecinos lejanos (C1)
```

**Complejidad:** O(V + E) donde V = vértices, E = aristas

---

#### `dfs(inicio_id)` - Búsqueda por Profundidad
Explora profundamente cada rama antes de pasar a la siguiente.

**¿Cuándo usarlo?**
- Detectar ciclos en el grafo
- Exploración exhaustiva de un camino
- Backtracking

**Ejemplo:**
```python
orden = grafo.dfs("P1")
# Resultado: ["P1", "R1", "C1", "H1"]
# Explora P1 → R1 → C1, luego retrocede a P1 → H1
```

**Complejidad:** O(V + E)

---

#### `dijkstra(inicio_id, objetivo_id=None)` - Caminos Más Cortos
Encuentra la distancia mínima desde un nodo a todos los demás.

**¿Cuándo usarlo?**
- Encontrar la ruta más eficiente (menor distancia)
- Calcular distancias a múltiples destinos
- Sistemas GPS, ruteo

**Retorna:**
- `dist`: Diccionario con distancias mínimas
- `prev`: Diccionario con predecesores (para reconstruir camino)

**Ejemplo:**
```python
dist, prev = grafo.dijkstra("P1")
# dist: {"P1": 0, "R1": 0.6, "H1": 0.5, "C1": 1.5}
# prev: {"P1": None, "R1": "P1", "H1": "P1", "C1": "R1"}
```

**Complejidad:** O((V + E) log V) con heap

---

#### `reconstruir_camino(prev, objetivo_id)` - Reconstrucción de Ruta
Usa los predecesores de Dijkstra para obtener el camino completo.

**Ejemplo:**
```python
camino = grafo.reconstruir_camino(prev, "C1")
# Resultado: ["P1", "R1", "C1"]
# Indica que la ruta es Panadería → Restaurante → Clínica
```

---

###  MÉTODOS DE INFORMACIÓN

#### `listar_nodos()`
Obtiene información de todos los lugares.
```python
nodos = grafo.listar_nodos()
# Retorna lista de diccionarios con todos los atributos de cada nodo
```

---

##  ESTRUCTURA DE `ejemplo.py`

###  FUNCIÓN `cargar_ejemplo()`

**Propósito:** Crear y configurar un grafo de demostración.

**Proceso:**
1. Crea un grafo no dirigido (bidireccional)
2. Define 4 lugares en forma de tuplas
3. Inserta cada lugar como nodo
4. Crea conexiones (aristas) entre lugares
5. Retorna el grafo configurado

**Lugares cargados:**
```
X → Usuario(0.0, Usuario)
P1 → Panadería La Delicia (0.8 km, Snack)
H1 → Hotel Mirador del Sol (1.2 km, Hotel)
C1 → Clínica Central Norte (1.8 km, Emergencia)
R1 → Restaurante El Sabor Local (2.4 km, Restaurante)
S1 → Cafetería Central ( 0.8 km, Snack)
```

**Conexiones creadas:**
```
X ←→ R1 (2.4 km)
X ←→ H1 (1.2 km)
X ←→ C1 (1.8 km)
X ←→ P1 (0.8 km)
X ←→ S1 (0.8 km)

P1 ←→ R1 (0.6 km)
P1 ←→ H1 (0.5 km)
H1 ←→ C1 (1.0 km)
R1 ←→ C1 (1.6 km)
S1 ←→ P1 (0.4 km)
S1 ←→ C1 (0.6 km)
```

**Nodo Eliminado:**
```
H1: "Hotel Mirador del Sol", 1.2, "Hotel".

```

**Conexiones Eliminadas:**
```
X ←→ C1 (1.8 km)
X ←→ H1 (1.2 km)
P1 ←→ H1 (0.5 km)
H1 ←→ C1 (1.0 km)

---

###  BLOQUE PRINCIPAL (`if __name__ == "__main__"`)

Ejecuta una demostración completa del sistema:

#### PASO 1: Listar nodos
Muestra todos los lugares disponibles con sus detalles.

#### PASO 2: Mostrar adyacencias
Visualiza todas las conexiones entre lugares.

#### PASO 3: Búsqueda BFS
Explora los lugares nivel por nivel.

#### PASO 4: Búsqueda DFS
Explora los lugares en profundidad.

#### PASO 5: Algoritmo de Dijkstra
Calcula distancias mínimas desde un lugar específico.

#### PASO 6: Reconstrucción de ruta
Muestra el camino más corto completo con detalles.

---

##  FLUJO DE EJECUCIÓN

```
┌─────────────────────────────────────────────────┐
│ INICIO: Ejecutar ejemplo.py                     │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │ cargar_ejemplo()    │
        │  (crea grafo)       │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
Insertar Nodos  Insertar     Retorna
            Aristas      Grafo


┌─────────────────────────────────────────────────┐
│ OPERACIONES EN EL GRAFO                         │
└─────────────────────────────────────────────────┘
    │
    ├─→ listar_nodos()
    │   (Muestra: X, P1, H1, C1, R1)
    │
    ├─→ listar_adyacencias()
    │   (Muestra conexiones)
    │
    ├─→ bfs("X")
    │   (Busca amplitud: [X, C1, H1, P1, R1])
    │
    ├─→ dfs("X")
    │   (Busca profundidad: [X, C1, H1, P1, R1])
    │
    ├─→ dijkstra("X")
    │   (Calcula caminos mínimos)
    │
    ├─→ reconstruir_camino(prev, "C1")
    │   (Muestra ruta: X → C1)
    │
    ├─→ eliminar una arista (ejemplo)
    │   (Muestra los datos anteriores con el cambio)
    │
    ├─→ eliminar un nodo (ejemplo)
    │   (Muestra los datos anteriores con el cambio)
    │
    └─→ Insertar un nuevo nodo (ejemplo)
        (Muestra los datos anteriores con el cambio)   
```

---

##  CONCEPTOS TEÓRICOS

### GRAFO
Estructura matemática compuesta por:
- **Nodos (Vértices)**: Puntos o lugares
- **Aristas (Edges)**: Conexiones entre nodos
- **Peso**: Valor asociado a cada arista (distancia)

### GRAFO DIRIGIDO vs NO DIRIGIDO
- **Dirigido**: A→B no implica B→A (calles de un sentido)
- **No dirigido**: A↔B (calles bidireccionales)

### LISTA DE ADYACENCIA
Estructura que almacena para cada nodo la lista de nodos vecinos.
Ejemplo: `{"P1": [("R1", 0.6), ("H1", 0.5)], ...}`

### BFS (Breadth-First Search)
- Explora nivel por nivel
- Encuentra caminos mínimos (en términos de aristas)
- Usa cola (FIFO)
- Tiempo: O(V + E)

### DFS (Depth-First Search)
- Explora profundamente antes de retroceder
- Detecta ciclos
- Usa pila (LIFO) - recursión
- Tiempo: O(V + E)

### ALGORITMO DE DIJKSTRA
- Encuentra caminos mínimos ponderados
- Usa cola de prioridad (heap)
- Requiere pesos no negativos
- Tiempo: O((V + E) log V)
- Uso real: GPS, ruteo de paquetes, mapas

---

##  EJEMPLOS DE USO

### Ejemplo 1: Buscar todos los hoteles
```python
g = cargar_ejemplo()
hoteles = g.buscar_por_categoria("Hotel")
for hotel in hoteles:
    print(f"Hotel encontrado: {hotel.nombre}")
```

### Ejemplo 2: Encontrar camino más corto
```python
g = cargar_ejemplo()
dist, prev = g.dijkstra("P1")
camino = g.reconstruir_camino(prev, "C1")
print(f"Ruta P1→C1: {camino}")
print(f"Distancia: {dist['C1']} km")
```

### Ejemplo 3: Explorar lugares cercanos
```python
g = cargar_ejemplo()
cercanos = g.bfs("P1")
print("Lugares accesibles desde P1:", cercanos)
```

### Ejemplo 4: Crear un nuevo grafo personalizado
```python
g = Grafo(dirigido=False)

# Agregar lugares
g.insertar_nodo(Nodo("A", "Lugar A", 1.0, "Tipo1"))
g.insertar_nodo(Nodo("B", "Lugar B", 2.0, "Tipo2"))

# Conectar
g.insertar_arista("A", "B", peso=1.5)

# Usar algoritmos
resultado_bfs = g.bfs("A")
```

---

##  CÓMO EJECUTAR

### Opción 1: Ejecutar ejemplo.py (recomendado)
```bash
python ejemplo.py
```
Muestra demostración completa con salida formateada.

### Opción 2: Ejecutar ejemplo_documentado.py (con comentarios detallados)
```bash
python ejemplo_documentado.py
```
Misma funcionalidad pero con más salida explicativa.

### Opción 3: Usar grafo.py como módulo
```python
from grafo import Grafo, Nodo

# Tu código personalizado aquí
g = Grafo()
g.insertar_nodo(...)
# etc.
```

---

##  ANÁLISIS DE COMPLEJIDAD

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| Insertar Nodo | O(1) | Acceso directo a diccionario |
| Eliminar Nodo | O(V + E) | Debe revisar todas las aristas |
| Insertar Arista | O(1) | Agregar a lista de adyacencia |
| Eliminar Arista | O(E) | Búsqueda en lista |
| BFS | O(V + E) | Visita cada nodo y arista |
| DFS | O(V + E) | Visita cada nodo y arista |
| Dijkstra | O((V + E) log V) | Con heap |
| Buscar por nombre | O(V) | Búsqueda lineal |

---

##  CONCLUSIÓN

Este sistema demuestra cómo:
- **grafo.py** proporciona la infraestructura y algoritmos
- **ejemplo.py** utiliza esa infraestructura para resolver un problema real
- Los **algoritmos de grafos** son fundamentales en sistemas de ruteo y navegación
- La **documentación y modularización** hacen el código mantenible y reutilizable

**Aplicaciones similares:**
- Google Maps (algoritmo de Dijkstra para rutas)
- Social Networks (grafos de amigos)
- Redes de computadoras (enrutamiento)
- Sistemas de recomendación

---