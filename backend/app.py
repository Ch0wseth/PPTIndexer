from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
from azure.search.documents import SearchClient

app = Flask(__name__)
CORS(app)

# Endpoint pour traiter le fichier
@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    upload_folder = './uploads'
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)

    try:
        # Sauvegarder le fichier
        file.save(file_path)

        # Lancer le script Python avec le fichier en paramètre
        result = subprocess.run(
            ['python', 'indexation.py', file_path],
            capture_output=True,
            text=True
        )

        # Vérifier si le script a échoué
        if result.returncode != 0:
            return jsonify({'success': False, 'logs': result.stderr}), 500

        # Retourner les logs du processus
        return jsonify({'success': True, 'logs': result.stdout})
    except Exception as e:
        return jsonify({'success': False, 'logs': str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)