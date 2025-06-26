"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Crear la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Manejo de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap automático
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros
@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

# Obtener o eliminar un miembro por ID
@app.route('/members/<int:member_id>', methods=['GET', 'DELETE'])
def member(member_id):
    response_body = {}

    if request.method == "GET":
        member = jackson_family.get_member(member_id)
        response_body['results'] = member if member else {}
        response_body['message'] = f'Datos del miembro de la familia {member_id}' if member else 'No se encontró el ID'
        status_code = 200 if member else 404
        return jsonify(response_body), status_code

    if request.method == "DELETE":
        member = jackson_family.delete_member(member_id)
        response_body['results'] = member
        response_body['message'] = f'El miembro {member_id} ha sido eliminado'
        return jsonify(response_body), 200

    # Manejo alternativo si el método no es GET ni DELETE
    response_body['message'] = 'Error desconocido'
    response_body['results'] = {}
    return jsonify(response_body), 403

# Agregar un nuevo miembro
@app.route('/members', methods=['POST'])
def add_family_member():
    data = request.get_json()

    # Validación simple
    if not data or 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({"message": "Datos incompletos"}), 400

    # Agregar el miembro
    new_member = jackson_family.add_member({
        "first_name": data['first_name'],
        "age": data['age'],
        "lucky_numbers": data['lucky_numbers']
    })

    response_body = {
        'message': 'Miembro agregado exitosamente',
        'member': new_member
    }
    return jsonify(response_body), 201

# Ejecutar el servidor si se ejecuta directamente
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
