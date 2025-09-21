# app.py
import os
from flask import Flask

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Define uma rota para a raiz do site ("/")
@app.route('/')
def hello_world():
    """Esta função responde à requisição na rota raiz."""
    return "Hello, World!"

if __name__ == "__main__":
    # Esta parte é para rodar localmente sem Docker, usando o servidor de desenvolvimento do Flask.
    # O Gunicorn usará a instância 'app' diretamente em produção.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))