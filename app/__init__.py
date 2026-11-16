from flask import Flask
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)

    # Carrega as configurações do projeto
    app.config.from_object(Config)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importa os modelos e cria as tabelas
    with app.app_context():
        from app import models
        db.create_all()

    return app
