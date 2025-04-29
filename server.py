# Importa las librerías necesarias
from flask import Flask, request, jsonify
import subprocess

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Cada vez que hacemos un POST a $URL/run se ejecuta run_command()
@app.route('/run', methods=['POST'])
def run_command():
    # Obtén el JSON enviado con la petición
    data = request.get_json()

    # Extrae el comando que viene en el JSON
    command = data.get('command')

    # Si no se proporciona un comando, devuelve un error 400 (Bad Request)
    if not command:
        return jsonify({"error": "No command provided"}), 400

    try:
        # Con subproccess se ejecuta el comando en la terminal
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Devuelve los resultados en formato JSON
        return jsonify({
            "stdout": result.stdout,        # Lo que imprimió el comando
            "stderr": result.stderr,        # Cualquier error que ocurriera
            "exitCode": result.returncode   # El código de salida del comando
        })

    except Exception as e:
        # Si ocurre un error al ejecutar el comando, devuelve un error 500 (Internal Server Error)
        return jsonify({"error": str(e)}), 500

# Inicia la aplicación Flask, escuchando en el puerto 3000
if __name__ == '__main__':
    app.run(port=3000)
