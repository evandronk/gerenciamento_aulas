import sqlite3

def criar_conexao_banco():
    # Conecta ao banco de dados (ou cria o arquivo banco_dados.db se não existir)
    conn = sqlite3.connect('banco_dados.db')
    criar_tabelas(conn)  # Certifica-se de que as tabelas existam
    return conn

def criar_tabelas(conn):
    cursor = conn.cursor()

    # Criar tabela professores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        ''')

    # Criar tabela restricoes_professor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restricoes_professor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_professor INTEGER NOT NULL,
            restricao_periodo INTEGER,
            restricao_horario TEXT,
            restricao_dia_semana TEXT,
            FOREIGN KEY(id_professor) REFERENCES professores(id_professor)
        )
        ''')

    # Criar tabela disciplinas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        periodo INTEGER,
        ch_semanal INTEGER,
        id_professor INTEGER,
        horario_periodo INTEGER,
        horario_horario TEXT,
        horario_dia_semana TEXT,
        sala_nome TEXT,
        FOREIGN KEY(id_professor) REFERENCES professores(id_professor),
        FOREIGN KEY(sala_nome) REFERENCES salas(nome)
    )
    ''')

    # Criar tabela horários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS horarios (
        id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
        periodo INTEGER,
        horario TEXT,
        dia_semana TEXT
    )
    ''')

    # Criar tabela salas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salas (
        nome TEXT PRIMARY KEY,
        capacidade INTEGER,
        tipo TEXT
    )
    ''')

    conn.commit()
