from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Base de datos de las 64 mesas (0=Libre, 1=Reservada)
mesas = {i: {"estado": 0, "expira": None} for i in range(1, 65)}

@app.route('/estado-mesas', methods=['GET'])
def ver_mesas():
    ahora = datetime.now()
    for i in mesas:
        if mesas[i]["expira"] and ahora > mesas[i]["expira"]:
            mesas[i]["estado"] = 0
            mesas[i]["expira"] = None
    return jsonify(mesas)

@app.route('/reservar-mesa', methods=['POST'])
def reservar():
    data = request.json
    n_mesa = int(data.get('mesa'))
    mesas[n_mesa]["estado"] = 1
    mesas[n_mesa]["expira"] = datetime.now() + timedelta(hours=2)
    return jsonify({"mensaje": f"Mesa {n_mesa} reservada"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)