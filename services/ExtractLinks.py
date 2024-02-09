from flask import request, jsonify
from flask_restful import Resource
import re

class Extract(Resource):
    def post(self):
        try:
            # Obtener los datos de la solicitud
            input_text = request.data.decode('utf-8')
            host = request.args.get('host')
            path = request.args.get('path')
            
            # Validar las entradas
            if not input_text or not host or not path:
                return jsonify(error='Input text, host, and path are required.'), 400

            # Agregar el host al path
            full_path = host + path
            
            # Compilar la expresión regular
            regex = re.compile(r'\[(.*?)\]')
            
            # Encontrar coincidencias en el texto de entrada
            matches = regex.findall(input_text)

            # Filtrar enlaces basados en el path completo
            filtered_links = [m for m in matches if m.startswith('/') or m.startswith(full_path)]

            # Eliminar el host del inicio de los enlaces
            # stripped_links = [link.replace(full_path, '', 1) if link.startswith(full_path) else link for link in filtered_links]

            # Devolver los enlaces filtrados
            return jsonify(filtered_links)

        except Exception as e:
            # Manejo de errores genérico
            return jsonify(error='An error occurred while processing the request.'), 500
