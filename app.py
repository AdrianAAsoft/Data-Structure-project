from flask import Flask, request, jsonify, render_template
from grafo import Grafo, crea_demo

app = Flask(__name__)

g = crea_demo()  # grafo de ejemplo

@app.route("/")
def index():
    return render_template("index.html")

# -------- Lecturas --------
@app.route("/paradas")
def paradas():
    return jsonify(g.paradas())

@app.route("/conexiones")
def conexiones():
    # arcos dirigidos (a -> b)
    return jsonify(g.arcos())

@app.route("/limpiarCo", methods=["POST"])
def limpiarC():
    try:
        g.limpiar_conexiones()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})


# -------- Mutaciones --------
@app.route("/agregar_parada", methods=["POST"])
def agregar_parada():
    data = request.get_json(force=True) or {}
    nombre = (data.get("nombre") or "").strip()
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre vacío"}), 400
    nom = g.agrega_parada(nombre)
    return jsonify({"ok": True, "nombre": nom})

@app.route("/agregar_conexion", methods=["POST"])
def agregar_conexion():
    data = request.get_json(force=True) or {}
    try:
        a = (data["a"] or "").strip()
        b = (data["b"] or "").strip()
        t = int(data["t"])
        bidir = bool(data.get("bidir", True))
    except (KeyError, ValueError):
        return jsonify({"ok": False, "error": "Datos inválidos"}), 400
    g.conecta(a, b, t, bidir=bidir)
    return jsonify({"ok": True})

@app.route("/eliminar_parada", methods=["POST"])
def eliminar_parada():
    data = request.get_json(force=True) or {}
    nombre = (data.get("nombre") or "").strip()
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre requerido"}), 400
    ok = g.elimina_parada(nombre)
    return jsonify({"ok": ok})

@app.route("/eliminar_conexion", methods=["POST"])
def eliminar_conexion():
    data = request.get_json(force=True) or {}
    try:
        a = (data["a"] or "").strip()
        b = (data["b"] or "").strip()
        bidir = bool(data.get("bidir", True))
    except KeyError:
        return jsonify({"ok": False, "error": "Datos inválidos"}), 400
    g.elimina_conexion(a, b, bidir=bidir)
    return jsonify({"ok": True})

# -------- Ruteo --------
@app.route("/ruta")
def ruta():
    ori = (request.args.get("ori") or "").strip()
    des = (request.args.get("des") or "").strip()
    if not ori or not des:
        return jsonify({"ok": False, "error": "Faltan 'ori' y/o 'des'"}), 400
    total, cam = g.dijkstra(ori, des)
    if total is None:
        return jsonify({"ok": False, "error": "No hay ruta", "tiempo": None, "camino": []}), 404
    return jsonify({"ok": True, "tiempo": int(total), "camino": cam})

# -------- Persistencia JSON --------
@app.route("/guardar", methods=["POST"])
def guardar():
    data = request.get_json(force=True) or {}
    ruta = data.get("ruta") or "grafo.json"
    ok, err = g.guardar_json(ruta)
    if not ok:
        return jsonify({"ok": False, "error": err}), 500
    return jsonify({"ok": True, "ruta": ruta})

@app.route("/cargar", methods=["POST"])
def cargar():
    data = request.get_json(force=True) or {}
    ruta = data.get("ruta") or "grafo.json"
    ok, err = g.cargar_json(ruta)
    if not ok:
        return jsonify({"ok": False, "error": err}), 500
    return jsonify({"ok": True, "ruta": ruta})

if __name__ == "__main__":
    app.run(debug=True)
