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
    data = request.json
    nom = g.agrega_parada(data.get("nombre", ""))
    return jsonify({"ok": True, "nombre": nom})

@app.route("/agregar_conexion", methods=["POST"])
def agregar_conexion():
    data = request.json
    g.conecta(data["a"], data["b"], int(data["t"]), bidir=data.get("bidir", True))
    return jsonify({"ok": True})

@app.route("/eliminar_parada", methods=["POST"])
def eliminar_parada():
    data = request.json
    ok = g.elimina_parada(data["nombre"])
    return jsonify({"ok": ok})

@app.route("/eliminar_conexion", methods=["POST"])
def eliminar_conexion():
    data = request.json
    g.elimina_conexion(data["a"], data["b"], bidir=data.get("bidir", True))
    return jsonify({"ok": True})

@app.route("/ruta", methods=["GET"])
def ruta():
    ori = request.args.get("ori")
    des = request.args.get("des")
    total, cam = g.dijkstra(ori, des)
    return jsonify({"tiempo": total, "camino": cam})

if __name__ == "__main__":
    app.run(debug=True)

