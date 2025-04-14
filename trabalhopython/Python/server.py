from flask import Flask, send_from_directory
from musica import musica_bp
import os
from flask_cors import CORS
import webbrowser
import threading        

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app, origins=["http://127.0.0.1:3333"])

app.register_blueprint(musica_bp)

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')


if __name__ == "__main__":
    threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:3333/')).start()
    app.run(debug=True, port=3333)
