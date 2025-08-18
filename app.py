from flask import Flask, request, jsonify, render_template
from grafo import Grafo, crea_demo

app = Flask(__name__)

g = crea_demo()  # Grafo inicial de ejemplo

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/paradas")
def paradas():
    return jsonify(g.paradas())

@app.route("/conexiones")
def conexiones():
    return jsonify(g.arcos())

@app.route("/agregar_parada", methods=["POST"])
def agregar_parada():
    data = request.get_json(force=True)
    nombre = (data or {}).get("nombre", "").strip()
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre vacío"}), 400
    nom = g.agrega_parada(nombre)
    return jsonify({"ok": True, "nombre": nom})

@app.route("/agregar_conexion", methods=["POST"])
def agregar_conexion():
    data = request.get_json(force=True) or {}
    try:
        a = data["a"]
        b = data["b"]
        t = int(data["t"])
        bidir = bool(data.get("bidir", True))
    except (KeyError, ValueError):
        return jsonify({"ok": False, "error": "Datos inválidos"}), 400

    ok, err = g.conecta(a, b, t, bidir=bidir)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True})

@app.route("/eliminar_parada", methods=["POST"])
def eliminar_parada():
    data = request.get_json(force=True) or {}
    nombre = data.get("nombre")
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre requerido"}), 400
    ok = g.elimina_parada(nombre)
    return jsonify({"ok": ok})

@app.route("/eliminar_conexion", methods=["POST"])
def eliminar_conexion():
    data = request.get_json(force=True) or {}
    try:
        a = data["a"]
        b = data["b"]
        bidir = bool(data.get("bidir", True))
    except KeyError:
        return jsonify({"ok": False, "error": "Datos inválidos"}), 400
    ok = g.elimina_conexion(a, b, bidir=bidir)
    return jsonify({"ok": ok})

@app.route("/ruta", methods=["GET"])
def ruta():
    ori = request.args.get("ori")
    des = request.args.get("des")
    if not ori or not des:
        return jsonify({"error": "Parámetros 'ori' y 'des' requeridos"}), 400
    if ori not in g.nodos or des not in g.nodos:
        return jsonify({"error": "Parada inexistente"}), 404
    total, cam = g.dijkstra(ori, des)
    if total is None:
        return jsonify({"tiempo": None, "camino": [], "ok": False, "error": "No hay ruta"}), 404
    return jsonify({"tiempo": total, "camino": cam, "ok": True})

if __name__ == "__main__":
    app.run(debug=True)
