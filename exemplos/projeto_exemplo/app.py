from flask import Flask, render_template
from flask_login import LoginManager
from models.base import db, init_db
from models.usuario import Usuario
from routes import register_blueprints
import os

def create_app():
    app = Flask(__name__)
    
    # Configuração
    app.config.from_object('config.Config')
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Configurar login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Criar diretório de uploads se não existir
    os.makedirs('static/uploads/perfil', exist_ok=True)
    
    # Rota principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
