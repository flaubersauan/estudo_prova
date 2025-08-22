from flask import *
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conexão com o banco
def get_db_connection():
    conn = sqlite3.connect("jogo.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/personagens/novo", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        jogo_origem = request.form["jogo_origem"]
        habilidade = request.form["habilidade_principal"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO personagens (nome, jogo_origem, habilidade_principal) VALUES (?, ?, ?)",
            (nome, jogo_origem, habilidade)
        )
        conn.commit()
        conn.close()

        return redirect("/personagens")

    return render_template("novo_personagem.html")

@app.route("/personagens")
def listar_personagens():
    conn = get_db_connection()
    personagens = conn.execute(
        "SELECT nome, jogo_origem, habilidade_principal FROM personagens"
    ).fetchall()
    conn.close()
    return render_template("lista_personagens.html", personagens=personagens)

if __name__ == "__main__":
    app.run(debug=True)

