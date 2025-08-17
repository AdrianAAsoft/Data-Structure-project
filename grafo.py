from heapq import heappush, heappop
from collections import defaultdict
import json

class Grafo:
    def __init__(self):
        # adj[a][b] = tiempo en min de a -> b
        self.adj = defaultdict(dict)

    # ---- Nodos ----
    def agrega_parada(self, nom):
        nom = nom.strip().lower()
        if nom and nom not in self.adj:
            self.adj[nom] = {}
        return nom

    def elimina_parada(self, nom):
        nom = nom.strip().lower()
        if nom in self.adj:
            self.adj.pop(nom, None)
            for x in list(self.adj.keys()):
                self.adj[x].pop(nom, None)
            return True
        return False

    def paradas(self):
        return sorted(self.adj.keys())

    # ---- Arcos (posible dirigido) ----
    def conecta(self, a, b, tiem, bidir=True):
        a, b = a.strip().lower(), b.strip().lower()
        if a not in self.adj:
            self.agrega_parada(a)
        if b not in self.adj:
            self.agrega_parada(b)
        self.adj[a][b] = int(tiem)
        if bidir:
            self.adj[b][a] = int(tiem)

    def elimina_conexion(self, a, b, bidir=True):
        a, b = a.strip().lower(), b.strip().lower()
        if a in self.adj:
            self.adj[a].pop(b, None)
        if bidir and b in self.adj:
            self.adj[b].pop(a, None)

    def arcos(self):
        lista = []
        for a in self.adj:
            for b, t in self.adj[a].items():
                lista.append((a, b, t))
        return sorted(lista)

    def conexiones(self):
        lista = []
        vistos = set()
        for a in self.adj:
            for b, t in self.adj[a].items():
                clave = tuple(sorted([a, b]))
                if clave not in vistos:
                    lista.append((a, b, t))
                    vistos.add(clave)
        return sorted(lista)

    # ---- Camino mas corto ----
    def dijkstra(self, ori, des):
        ori, des = ori.strip().lower(), des.strip().lower()
        if ori not in self.adj or des not in self.adj:
            return None, []

        dist = {n: float('inf') for n in self.adj}
        prev = {n: None for n in self.adj}
        dist[ori] = 0

        pq = []
        heappush(pq, (0, ori))

        while pq:
            d, u = heappop(pq)
            if d > dist[u]:
                continue
            if u == des:
                break
            for v, w in self.adj[u].items():
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heappush(pq, (nd, v))

        if dist[des] == float('inf'):
            return None, []

        cam = []
        cur = des
        while cur is not None:
            cam.append(cur)
            cur = prev[cur]
        cam.reverse()
        return dist[des], cam

    # ---- IO JSON ----
    def a_dict(self):
        return {
            "nodos": sorted(self.adj.keys()),
            "arcos": [{"a": a, "b": b, "t": int(t)} for a, b, t in self.arcos()],
        }

    def desde_dict(self, data):
        self.adj.clear()
        for n in data.get("nodos", []):
            self.agrega_parada(n)
        for arco in data.get("arcos", []):
            a = arco.get("a", ""); b = arco.get("b", ""); t = arco.get("t", 0)
            if a and b:
                self.conecta(a, b, int(t), bidir=False)

    def guardar_json(self, ruta):
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(self.a_dict(), f, ensure_ascii=False, indent=2)
            return True, None
        except Exception as e:
            return False, str(e)

    def cargar_json(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.desde_dict(data)
            return True, None
        except Exception as e:
            return False, str(e)

    def muestra(self):
        print("Grafo (lista de adyacencia):")
        for a in sorted(self.adj.keys()):
            vecinos = ", ".join(f"{b}({t}m)" for b, t in sorted(self.adj[a].items()))
            print(f"  {a} -> {vecinos}")
        print("")


# ---- Demo base ----
def crea_demo():
    g = Grafo()
    base = ["universidad", "supermercado", "hospital", "mall", "escuela"]
    for p in base:
        g.agrega_parada(p)
    g.conecta("universidad", "supermercado", 7)
    g.conecta("universidad", "hospital", 10)
    g.conecta("supermercado", "mall", 6)
    g.conecta("hospital", "mall", 5)
    g.conecta("hospital", "escuela", 8)
    g.conecta("mall", "escuela", 12)
    g.conecta("supermercado", "escuela", 15)
    g.conecta("mall", "universidad", 20, bidir=False)
    return g
