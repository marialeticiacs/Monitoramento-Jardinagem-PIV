from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

API_URL = 'http://localhost:5002/api'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        response = requests.post(f'{API_URL}/login', json={'email': email, 'senha': senha})
        if response.status_code == 200:
            session['token'] = response.json()['access_token']
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'api_key': request.form['api_key'],
            'planta_id': request.form['planta_id'],
            'senha': request.form['senha']
        }
        response = requests.post(f'{API_URL}/register_user', json=user)
        if response.status_code == 201:
            flash('Usuário cadastrado com sucesso', 'success')
            return redirect(url_for('login'))
        else:
            flash('Erro ao cadastrar usuário', 'danger')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)