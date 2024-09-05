import sqlite3

from db.db_conn import criar_conexao_banco


def conectar():
    return sqlite3.connect('banco_dados.db')


def verificar_professor_existente(nome):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM professores WHERE nome = ?
    ''', (nome,))

    resultado = cursor.fetchone()[0]
    conn.close()

    return resultado > 0


def salvar_professor(nome, restricoes=None):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    # Inserir o professor sem especificar id_professor; será gerado automaticamente
    cursor.execute('''
        INSERT INTO professores (nome)
        VALUES (?)
    ''', (nome,))

    # Recuperar o id_professor gerado automaticamente
    id_professor = cursor.lastrowid

    # Inserir as restrições na tabela restricoes_professor
    for restricao in restricoes or []:
        restricao_periodo = restricao.periodo
        restricao_horario = str(restricao.horario)
        restricao_dia_semana = restricao.dia_semana

        cursor.execute('''
            INSERT INTO restricoes_professor (id_professor, restricao_periodo, restricao_horario, restricao_dia_semana)
            VALUES (?, ?, ?, ?)
        ''', (id_professor, restricao_periodo, restricao_horario, restricao_dia_semana))

    conn.commit()
    conn.close()


def editar_professor(id_professor, nome=None, restricao=None):
    conn = conectar()
    cursor = conn.cursor()

    if nome:
        cursor.execute('''
            UPDATE professores
            SET nome = ?
            WHERE id_professor = ?
        ''', (nome, id_professor))

    if restricao:
        restricao_periodo = 0
        restricao_horario = str(restricao.horario)
        restricao_dia_semana = restricao.dia_semana
        cursor.execute('''
            UPDATE professores
            SET restricao_periodo = ?, restricao_horario = ?, restricao_dia_semana = ?
            WHERE id_professor = ?
        ''', (restricao_periodo, restricao_horario, restricao_dia_semana, id_professor))

    conn.commit()
    conn.close()

def excluir_professor(id_professor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM professores WHERE id_professor = ?
    ''', (id_professor,))

    conn.commit()
    conn.close()

def obter_id_professor_por_nome(nome_professor):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_professor 
        FROM professores 
        WHERE nome = ?
    """, (nome_professor,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0]  # Retorna o id do professor
    else:
        raise ValueError(f"Professor {nome_professor} não encontrado no banco de dados.")


def obter_professores():
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id_professor, nome FROM professores")
    professores = cursor.fetchall()
    conn.close()

    return professores


def obter_restricoes_professor(id_professor):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    # Execute a query para selecionar todas as restrições do professor na tabela correta
    cursor.execute("""
        SELECT restricao_dia_semana, restricao_horario 
        FROM restricoes_professor 
        WHERE id_professor = ?
    """, (id_professor,))

    restricoes = cursor.fetchall()

    conn.close()
    return restricoes


def salvar_restricoes_professor(id_professor, lista_restricoes):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    # Primeiro, exclua todas as restrições existentes para esse professor na tabela correta
    cursor.execute("DELETE FROM restricoes_professor WHERE id_professor = ?", (id_professor,))

    # Em seguida, insira as novas restrições
    if lista_restricoes:
        cursor.executemany("""
            INSERT INTO restricoes_professor (id_professor, restricao_dia_semana, restricao_horario, restricao_periodo) 
            VALUES (?, ?, ?, ?)
        """, [(id_professor, restricao.dia_semana, restricao.horario[0], restricao.periodo) for restricao in
              lista_restricoes])

    conn.commit()
    conn.close()

def excluir_professor_com_restricoes(id_professor):
    conn = criar_conexao_banco()
    cursor = conn.cursor()

    # Remover as restrições do professor na tabela restricoes_professor
    cursor.execute("DELETE FROM restricoes_professor WHERE id_professor = ?", (id_professor,))

    # Remover o professor da tabela professores
    cursor.execute("DELETE FROM professores WHERE id_professor = ?", (id_professor,))

    conn.commit()
    conn.close()


def obter_professores_com_disciplinas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nome, d.periodo, d.nome, d.ch_semanal 
        FROM professores p
        LEFT JOIN disciplinas d ON p.id_professor = d.id_professor
    ''')

    dados = cursor.fetchall()

    professores = {}
    for nome, periodo, disciplina_nome, ch_semanal in dados:
        if nome not in professores:
            professores[nome] = {
                'nome': nome,
                'disciplinas': []
            }
        if disciplina_nome:
            professores[nome]['disciplinas'].append({
                'periodo': periodo,
                'nome': disciplina_nome,
                'ch_semanal': ch_semanal
            })

    conn.close()

    return list(professores.values())