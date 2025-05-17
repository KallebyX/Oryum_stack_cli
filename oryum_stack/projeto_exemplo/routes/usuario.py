from flask import Blueprint
from controllers.usuario_controller import UsuarioController
from flask_login import login_required

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

# Listar todos os usuários
usuario_bp.route('/', methods=['GET'])(UsuarioController.index)

# Exibir formulário de criação
usuario_bp.route('/create', methods=['GET'])(UsuarioController.create)

# Salvar novo usuário
usuario_bp.route('/', methods=['POST'])(UsuarioController.store)

# Exibir detalhes de um usuário
usuario_bp.route('/<int:id>', methods=['GET'])(UsuarioController.show)

# Exibir formulário de edição
usuario_bp.route('/<int:id>/edit', methods=['GET'])(UsuarioController.edit)

# Atualizar usuário
usuario_bp.route('/<int:id>', methods=['POST', 'PUT', 'PATCH'])(UsuarioController.update)

# Remover usuário
usuario_bp.route('/<int:id>/delete', methods=['POST', 'DELETE'])(UsuarioController.destroy)
