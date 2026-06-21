-- ***! Arquivo: banco.sql ***!
-- ***! Schema do banco de dados SQLite - Sistema Sabor & Arte ***!

CREATE TABLE IF NOT EXISTS garcom (
    id_garcom   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    matricula   TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    preco       REAL NOT NULL,
    categoria   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido   INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_mesa INTEGER NOT NULL,
    id_garcom   INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'aberto',
    FOREIGN KEY (id_garcom) REFERENCES garcom(id_garcom)
);

-- ***! Tabela de relacionamento N:N entre Pedido e Produto (Agregação) ***!
CREATE TABLE IF NOT EXISTS pedido_produto (
    id_pedido   INTEGER NOT NULL,
    id_produto  INTEGER NOT NULL,
    FOREIGN KEY (id_pedido)  REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);
