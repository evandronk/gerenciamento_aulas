import sqlite3

def conectar():
    return sqlite3.connect('banco_dados.db')

def salvar_sala(nome, capacidade, tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO salas (nome, capacidade, tipo)
        VALUES (?, ?, ?)
    ''', (nome, capacidade, tipo))

    conn.commit()
    conn.close()

def editar_sala(nome, capacidade=None, tipo=None):
    conn = conectar()
    cursor = conn.cursor()

    if capacidade is not None:
        cursor.execute('''
            UPDATE salas
            SET capacidade = ?
            WHERE nome = ?
        ''', (capacidade, nome))

    if tipo is not None:
        cursor.execute('''
            UPDATE salas
            SET tipo = ?
            WHERE nome = ?
        ''', (tipo, nome))

    conn.commit()
    conn.close()

def excluir_sala(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM salas WHERE nome = ?
    ''', (nome,))

    conn.commit()
    conn.close()
