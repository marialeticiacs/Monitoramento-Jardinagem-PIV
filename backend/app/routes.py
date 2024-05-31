from flask import Blueprint
from app.controllers.user_controller import register_user, login_user, get_users, get_user, update_user, delete_user
from app.controllers.sensor_controller import receive_data
from flask_jwt_extended import jwt_required

routes = Blueprint('routes', __name__)

# Rotas de usuário com autenticação JWT
routes.route('/register_user', methods=['POST'])(register_user)
routes.route('/login', methods=['POST'])(login_user)
routes.route('/users', methods=['GET'])(jwt_required()(get_users))
routes.route('/user/<email>', methods=['GET'])(jwt_required()(get_user))
routes.route('/users/<user_id>', methods=['PUT'])(jwt_required()(update_user))
routes.route('/users/<user_id>', methods=['DELETE'])(jwt_required()(delete_user))

# Rota do sensor sem autenticação JWT
routes.route('/receive_data', methods=['POST'])(receive_data)
