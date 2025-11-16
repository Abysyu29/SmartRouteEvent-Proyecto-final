# Proyecto: SmartRoute Event (Versión 3 - Grafos)
# Integrantes:
# Sergio Andres Martinez Cifuentes 2242039
# Andres Felipe Guaqueta Rojas 2242034
# Andres Sebastian Pinzon Gutierrez 2221887
# Daniel Eduardo Rincon Arias 2202316

"""
Ejemplo de uso del grafo para lugares cercanos.

Aquí se demuestra cómo utilizar la clase Grafo para:
1. Cargar lugares (nodos) con información detallada
2. Crear conexiones entre lugares (aristas)
3. Ejecutar algoritmos de búsqueda y enrutamiento
4. Encontrar caminos óptimos entre lugares
"""

from grafo import Grafo, Nodo # type: ignore


# FUNCIÓN: cargar_ejemplo

def cargar_ejemplo():
    """
    Crea y retorna un grafo con lugares cercanos.
    
    Este grafo simula un área urbana con 4 lugares de interés:
    - Panadería (P1)
    - Hotel (H1)
    - Clínica (C1)
    - Restaurante (R1)
    
    Las conexiones entre lugares representan caminos y sus distancias.
    
    Retorna:
        Grafo: Un grafo no dirigido con los lugares y sus conexiones
    """
    
    # Crear un grafo NO DIRIGIDO (las conexiones funcionan en ambas direcciones)
    g = Grafo(dirigido=False)

    # PASO 1: DEFINIR LOS LUGARES (NODOS)
    
    # Cada lugar tiene 5 atributos:
    # - ID único: identificador para referencias rápidas
    # - Nombre: nombre legible del lugar
    # - Distancia: kilómetros desde un punto de referencia (ej: centro ciudad)
    # - Tiempo: estimación de tiempo de viaje
    # - Categoría: tipo de lugar para clasificación
    
    datos = [
        # (ID, Nombre, Distancia_km, Tiempo_viaje, Categoría)
        ("C1", "Clínica Central Norte", 1.8, "6 min en carro", "Emergencia"),
        ("H1", "Hotel Mirador del Sol", 1.2, "15 min caminando", "Hotel"),
        ("P1", "Panadería La Delicia", 0.8, "10 min caminando", "Snack"),
        ("R1", "Restaurante El Sabor Local", 2.4, "8 min caminando", "Restaurante"),
    ]

    # Crear e insertar cada lugar en el grafo
    for node_id, nombre, dist, tiempo, cat in datos:
        # Crear el nodo con los datos
        nodo = Nodo(node_id, nombre, dist, tiempo, cat)
        # Agregar el nodo al grafo
        g.insertar_nodo(nodo)

    
    # PASO 2: CREAR CONEXIONES ENTRE LUGARES (ARISTAS)
    
    # Cada arista tiene un peso que representa la distancia entre lugares
    # Las conexiones son bidireccionales (grafo no dirigido)
    
    # Panadería (P1) está cerca del Restaurante (R1)
    # Distancia entre ellos: 0.6 km
    g.insertar_arista("P1", "R1", peso=0.6)
    
    # Panadería (P1) está cerca del Hotel (H1)
    # Distancia entre ellos: 0.5 km
    g.insertar_arista("P1", "H1", peso=0.5)
    
    # Hotel (H1) está cerca de la Clínica (C1)
    # Distancia entre ellos: 1.0 km
    g.insertar_arista("H1", "C1", peso=1.0)
    
    # Restaurante (R1) está cerca de la Clínica (C1)
    # Distancia entre ellos: 1.6 km
    g.insertar_arista("R1", "C1", peso=1.6)

    return g



# BLOQUE PRINCIPAL: PRUEBAS

if __name__ == "__main__":
    """
    Ejecuta el programa cuando se corre directamente.
    Demuestra todas las funcionalidades del grafo.
    """
    
    # Cargar los datos de ejemplo
    print("=" * 70)
    print("SISTEMA DE LUGARES CERCANOS - SmartRoute Event")
    print("=" * 70)
    
    g = cargar_ejemplo()
    
    
    # 1. LISTAR TODOS LOS NODOS (LUGARES DISPONIBLES)
    
    print("\n📍 NODOS CARGADOS:")
    print("-" * 70)
    # Obtener información de todos los lugares
    nodos_info = g.listar_nodos()
    for i, nodo in enumerate(nodos_info, 1):
        print(f"{i}. {nodo['nombre']}")
        print(f"   ID: {nodo['id']}")
        print(f"   Categoría: {nodo['categoria']}")
        print(f"   Distancia: {nodo['distancia_km']} km")
        print(f"   Tiempo estimado: {nodo['tiempo_str']}")

    
    # 2. MOSTRAR ADYACENCIAS (QUÉ ESTÁ CONECTADO CON QUÉ)
    
    print("\n🔗 ADYACENCIAS (CONEXIONES ENTRE LUGARES):")
    print("-" * 70)
    # Obtener la estructura de adyacencia
    adyacencias = g.listar_adyacencias()
    for nodo_origen, conexiones in adyacencias.items():
        # Encontrar el nombre del nodo origen para mejor legibilidad
        nodo_obj = g.buscar_nodo_por_id(nodo_origen)
        nombre_origen = nodo_obj.nombre if nodo_obj else nodo_origen
        
        print(f"\nDesde {nombre_origen} ({nodo_origen}):")
        for destino, peso, meta in conexiones:
            nodo_dest = g.buscar_nodo_por_id(destino)
            nombre_destino = nodo_dest.nombre if nodo_dest else destino
            print(f"  → {nombre_destino} ({destino}): {peso} km")

    
    # 3. BÚSQUEDA POR AMPLITUD (BFS)
    
    print("\n\n🔍 BÚSQUEDA POR AMPLITUD (BFS) desde Panadería (P1):")
    print("-" * 70)
    # BFS visita todos los nodos nivel por nivel
    # Útil para encontrar caminos cortos sin considerar pesos
    bfs_resultado = g.bfs("P1")
    print(f"Orden de visita: {bfs_resultado}")
    
    # Mostrar información de los lugares visitados
    print("\nLugares encontrados:")
    for nodo_id in bfs_resultado:
        nodo = g.buscar_nodo_por_id(nodo_id)
        print(f"  - {nodo.nombre} ({nodo_id})")

    
    # 4. BÚSQUEDA POR PROFUNDIDAD (DFS)
    
    print("\n\n🔍 BÚSQUEDA POR PROFUNDIDAD (DFS) desde Panadería (P1):")
    print("-" * 70)
    # DFS explora lo más profundo posible antes de retroceder
    # Útil para detectar ciclos y explorar de manera diferente
    dfs_resultado = g.dfs("P1")
    print(f"Orden de visita: {dfs_resultado}")
    
    # Mostrar información de los lugares visitados
    print("\nLugares encontrados:")
    for nodo_id in dfs_resultado:
        nodo = g.buscar_nodo_por_id(nodo_id)
        print(f"  - {nodo.nombre} ({nodo_id})")

    
    # 5. ALGORITMO DE DIJKSTRA (CAMINOS MÁS CORTOS)
    
    print("\n\n📍 ALGORITMO DE DIJKSTRA (CAMINOS MÁS CORTOS desde P1):")
    print("-" * 70)
    # Dijkstra encuentra el camino con menor distancia/peso
    # Devuelve distancias mínimas y predecesores de cada nodo
    dist, prev = g.dijkstra("P1")
    
    print("Distancias mínimas desde la Panadería:")
    for nodo_id, distancia in dist.items():
        nodo = g.buscar_nodo_por_id(nodo_id)
        nombre = nodo.nombre if nodo else nodo_id
        if distancia == float('inf'):
            print(f"  {nombre} ({nodo_id}): NO ALCANZABLE")
        else:
            print(f"  {nombre} ({nodo_id}): {distancia:.2f} km")

    
    # 6. RECONSTRUIR CAMINO ÓPTIMO (P1 -> C1)
    
    print("\n\n🗺️  CAMINO MÁS CORTO: Panadería (P1) → Clínica (C1):")
    print("-" * 70)
    # Usar los predecesores para reconstruir el camino completo
    camino = g.reconstruir_camino(prev, "C1")
    
    print(f"Ruta óptima: {' → '.join(camino)}")
    print("\nDetalle del camino:")
    distancia_total = 0
    for i in range(len(camino) - 1):
        nodo_actual = camino[i]
        nodo_siguiente = camino[i + 1]
        
        # Buscar el peso de la arista entre estos nodos
        for destino, peso, meta in g.listar_adyacencias()[nodo_actual]:
            if destino == nodo_siguiente:
                # Obtener nombres para mostrar
                nodo_obj1 = g.buscar_nodo_por_id(nodo_actual)
                nodo_obj2 = g.buscar_nodo_por_id(nodo_siguiente)
                nombre1 = nodo_obj1.nombre if nodo_obj1 else nodo_actual
                nombre2 = nodo_obj2.nombre if nodo_obj2 else nodo_siguiente
                
                distancia_total += peso
                print(f"  {i + 1}. {nombre1} → {nombre2}: {peso} km")
                break
    
    print(f"\n✅ Distancia total: {distancia_total:.2f} km")
    print("=" * 70)
