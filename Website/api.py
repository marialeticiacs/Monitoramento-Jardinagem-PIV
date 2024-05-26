from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId
import certifi

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://marialeticia:mleticia2005@cluster-piv.rr2y51m.mongodb.net/DB_PIV?retryWrites=true&w=majority&tlsCAFile={}".format(certifi.where())
app.config['SECRET_KEY'] = 'supersecretkey'

mongo = PyMongo(app)

@app.route('/api/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['nome', 'email', 'telefone', 'api_key', 'planta_id', 'senha']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Campos obrigatórios ausentes'}), 400
    
    print("Recebendo requisição de registro de usuário...")
    print("Dados recebidos:", data)

    hashed_password = generate_password_hash(data['senha'], method='pbkdf2:sha256')
    user = {
        'nome': data['nome'],
        'email': data['email'],
        'telefone': data['telefone'],
        'api_key': data['api_key'],
        'planta_id': data['planta_id'],
        'senha': hashed_password
    }
    
    print("Usuário a ser inserido no banco de dados:", user)

    try:
        db = mongo.db  # Certifique-se de acessar o banco de dados correto
        if db.users.find_one({'email': user['email']}):
            return jsonify({'message': 'Email já cadastrado'}), 409
        
        db.users.insert_one(user)
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    except Exception as e:
        print("Erro durante o registro de usuário:", str(e))
        return jsonify({'message': 'Erro ao cadastrar usuário'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        db = mongo.db  # Certifique-se de acessar o banco de dados correto
        user = db.users.find_one({'email': data['email']})
        
        if user and check_password_hash(user['senha'], data['senha']):
            token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'access_token': token}), 200
        
        return jsonify({'message': 'Credenciais inválidas'}), 401
    except Exception as e:
        print("Erro durante o login:", str(e))
        return jsonify({'message': 'Erro ao fazer login'}), 500

@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token está faltando!'}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        db = mongo.db  # Certifique-se de acessar o banco de dados correto
        current_user = db.users.find_one({'_id': ObjectId(data['user_id'])})
        if not current_user:
            raise Exception("Usuário não encontrado")
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token é inválido!'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 401

    return dumps(current_user), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)