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
        bidir = bool(data.get(
