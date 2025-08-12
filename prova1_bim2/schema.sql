CREATE TABLE IF NOT EXISTS personagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    jogo_origem TEXT NOT NULL,
    habilidade_principal TEXT NOT NULL
);
