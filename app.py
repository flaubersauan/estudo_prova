from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from modelos import User

app = Flask(__name__)
app.secret_key = 'guilherme'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

produtos = [
    {'nome': 'Notebook', 'preco': 3500.00},
    {'nome': 'Mouse Gamer', 'preco': 150.00},
    {'nome': 'Teclado Mecânico', 'preco': 250.00},
    {'nome': 'Monitor 24"', 'preco': 899.90}
]


# Carregador de usuário
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        session['usuarios'] = {}
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuarios = session.get('usuarios', {})

        if nome in usuarios and usuarios[nome] == senha:
            user = User(nome, senha)
            login_user(user)
            return redirect(url_for('dash'))

        flash('Nome ou senha inválidos.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuarios = session.get('usuarios', {})

        if nome not in usuarios:
            usuarios[nome] = senha
            session['usuarios'] = usuarios

            user = User(nome, senha)
            login_user(user)
            return redirect(url_for('dash'))

        flash('Nome já cadastrado.', 'error')
        return redirect(url_for('register'))
    return render_template('cadastro.html')
    
@app.route('/dash')
@login_required
def dash():
    nome = current_user.nome
    return render_template('dashboard.html', nome=nome)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/produtos')
@login_required
def listar_produtos():
    return render_template('produtos.html', produtos=produtos)


@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar_ao_carrinho():
    nome_produto = request.form.get('nome')
    # pegar carrinho do usuário logado
    carrinhos = session.get('carrinhos', {})  # dicionário: user_id -> lista de produtos
    user_id = current_user.get_id()

    carrinho_usuario = carrinhos.get(user_id, [])

    for produto in produtos:
        if produto['nome'] == nome_produto:
            carrinho_usuario.append({'nome': nome_produto})
            break

    carrinhos[user_id] = carrinho_usuario
    session['carrinhos'] = carrinhos

    return redirect(url_for('listar_produtos'))

@app.route('/carrinho')
@login_required
def ver_carrinho():
    carrinhos = session.get('carrinhos', {})
    user_id = current_user.get_id()
    carrinho_usuario = carrinhos.get(user_id, [])
    return render_template('carrinho.html', carrinho=carrinho_usuario)


