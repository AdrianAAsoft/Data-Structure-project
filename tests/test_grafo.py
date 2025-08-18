from grafo import Grafo, crea_demo

def test_crea_demo_y_camino():
    g = crea_demo()
    t, cam = g.dijkstra("universidad", "escuela")
    assert t is not None
    assert cam[0] == "universidad"
    assert cam[-1] == "escuela"

def test_crud():
    g = Grafo()
    g.agrega_parada("A"); g.agrega_parada("B")
    g.conecta("A","B",5,bidir=False)
    assert ("a","b",5) in g.arcos()
    g.elimina_conexion("A","B",bidir=False)
    assert ("a","b",5) not in g.arcos()
    g.elimina_parada("A")
    assert "a" not in g.paradas()

def test_json_roundtrip(tmp_path):
    g = crea_demo()
    ruta = tmp_path/"g.json"
    ok,_ = g.guardar_json(str(ruta))
    assert ok
    g2 = Grafo()
    ok,_ = g2.cargar_json(str(ruta))
    assert ok
    assert set(g.paradas()) == set(g2.paradas())
