from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Aquí se guardarán las reservas temporalmente
reservas = []

@app.route('/reservar', methods=['POST'])
def crear_reserva():
    datos = request.json
    datos['estado'] = 'Pendiente' # Todas entran por confirmar
    reservas.append(datos)
    return jsonify({"mensaje": "Reserva recibida", "id": len(reservas)-1}), 200

@app.route('/admin/reservas', methods=['GET'])
def ver_reservas():
    return jsonify(reservas), 200

@app.route('/admin/confirmar/<int:id>', methods=['POST'])
def confirmar_reserva(id):
    if 0 <= id < len(reservas):
        reservas[id]['estado'] = 'Confirmada'
        return jsonify({"mensaje": "Reserva confirmada"}), 200
    return jsonify({"error": "No encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
