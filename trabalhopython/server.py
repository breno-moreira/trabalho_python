from flask import Flask, send_from_directory
from musica import musica_bp  # Alterado para importar o Blueprint de músicas
import os
from flask_cors import CORS

app = Flask( _titulo_,static_url_path='', static_folder='static')
CORS(app, origins=["http://localhost:5000"])

# Registro do blueprint de músicas
app.register_blueprint(musica_bp)

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

if _titulo_ == "_main_":
    app.run(debug=True)