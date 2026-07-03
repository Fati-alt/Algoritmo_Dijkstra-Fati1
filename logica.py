# logica.py
import heapq

class SistemaPolinizacion:
    def __init__(self):
        # Definimos los nodos (Flores) y sus coordenadas (X, Y) para dibujarlos después
        self.nodos = {
            "Colmena": (80, 200),
            "Flor A": (220, 100),
            "Flor B": (220, 300),
            "Flor C": (400, 100),
            "Flor D": (400, 300),
            "Flor E": (550, 200)
        }
        
        # Lista de conexiones (origen, destino, costo/distancia)
        self.aristas = [
            ("Colmena", "Flor A", 4),
            ("Colmena", "Flor B", 6),
            ("Flor A", "Flor B", 2),
            ("Flor A", "Flor C", 3),
            ("Flor B", "Flor D", 5),
            ("Flor C", "Flor D", 1),
            ("Flor C", "Flor E", 4),
            ("Flor D", "Flor E", 2)
        ]

    def calcular_dijkstra(self, inicio, fin):
        # Construir lista de adyacencia a partir de las aristas
        grafo = {nodo: [] for nodo in self.nodos}
        for u, v, peso in self.aristas:
            grafo[u].append((v, peso))
            grafo[v].append((u, peso)) # Grafo no dirigido

        # Algoritmo de Dijkstra estándar
        cola = [(0, inicio, [inicio])]
        visitados = set()

        while cola:
            (costo, actual, camino) = heapq.heappop(cola)
            
            if actual in visitados:
                continue
            visitados.add(actual)

            if actual == fin:
                return camino, costo

            for vecino, peso in grafo[actual]:
                if vecino not in visitados:
                    heapq.heappush(cola, (costo + peso, vecino, camino + [vecino]))
                    
        return [], 0
