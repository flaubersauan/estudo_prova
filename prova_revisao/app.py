from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'chave_secreta'

def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Definindo a classe de User para o Flask-Login
class User(UserMixin):
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE nome = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()
        if resultado:
            user = User(nome=resultado['nome'], senha=resultado['senha'])
            user.id = resultado['nome']
            return user
        return None

# Função do Flask-Login para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']
        senha_hash = generate_password_hash(senha)  # Gerando o hash da senha

        conexao = obter_conexao()

        # Verifica se o usuário já existe
        sql = "SELECT * FROM users WHERE nome = ?"
        resultado = conexao.execute(sql, (nome,)).fetchone()

        if resultado:
            # Se o usuário já existe
            flash('Nome de usuário já existe!', category='error')
            conexao.close()  # Fecha a conexão
            return redirect(url_for('register'))

        # Se o usuário não existe, faz o cadastro
        sql = "INSERT INTO users (nome, senha) VALUES (?, ?)"
        conexao.execute(sql, (nome, senha_hash))
        conexao.commit()  # Commit para salvar no banco
        conexao.close()  # Fecha a conexão após a inserção

        # Faz o login do usuário automaticamente após o cadastro
        user = User(nome=nome, senha=senha_hash)
        user.id = nome
        login_user(user)

        flash('Cadastro realizado com sucesso!', category='success')
        return redirect(url_for('dash'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']

        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE nome = ?"
        resultado = conexao.execute(sql, (nome,)).fetchone()
        conexao.close()

        if resultado and check_password_hash(resultado['senha'], senha):
            user = User(nome=nome, senha=resultado['senha'])
            user.id = nome
            login_user(user)
            return redirect(url_for('dash'))

        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
