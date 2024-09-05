import sqlite3

def conectar():
    return sqlite3.connect('banco_dados.db')

def salvar_horario(periodo, horario, dia_semana):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO horarios (periodo, horario, dia_semana)
        VALUES (?, ?, ?)
    ''', (periodo, str(horario), dia_semana))

    conn.commit()
    conn.close()

def editar_horario(id_horario, periodo=None, horario=None, dia_semana=None):
    conn = conectar()
    cursor = conn.cursor()

    if periodo is not None:
        cursor.execute('''
            UPDATE horarios
            SET periodo = ?
            WHERE id_horario = ?
        ''', (periodo, id_horario))

    if horario is not None:
        cursor.execute('''
            UPDATE horarios
            SET horario = ?
            WHERE id_horario = ?
        ''', (str(horario), id_horario))

    if dia_semana is not None:
        cursor.execute('''
            UPDATE horarios
            SET dia_semana = ?
            WHERE id_horario = ?
        ''', (dia_semana, id_horario))

    conn.commit()
    conn.close()

def excluir_horario(id_horario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM horarios WHERE id_horario = ?
    ''', (id_horario,))

    conn.commit()
    conn.close()


def obter_periodos_disponiveis():
    conn = conectar()
    cursor = conn.cursor()

    # Buscar os períodos únicos das disciplinas
    cursor.execute('''
        SELECT DISTINCT periodo FROM disciplinas
    ''')

    periodos = cursor.fetchall()
    conn.close()

    # Retornar a lista de períodos disponíveis
    return [periodo[0] for periodo in periodos]

def obter_disciplinas_por_periodo(periodo=None):
    conn = conectar()
    cursor = conn.cursor()

    if periodo is None:
        # Consulta para pegar todas as disciplinas, incluindo o id_disciplina
        cursor.execute('''
            SELECT id_disciplina, nome, ch_semanal, periodo FROM disciplinas
        ''')
    else:
        # Consulta para pegar as disciplinas de um período específico
        cursor.execute('''
            SELECT id_disciplina, nome, ch_semanal FROM disciplinas WHERE periodo = ?
        ''', (periodo,))

    disciplinas = cursor.fetchall()
    conn.close()

    # Verifique se o retorno inclui id_disciplina
    print(f"Disciplinas retornadas: {disciplinas}")

    # Retorna a lista de disciplinas, agora incluindo o id_disciplina
    if periodo is None:
        return [{'id_disciplina': id_disciplina, 'nome': nome, 'ch_semanal': ch_semanal, 'periodo': periodo} for id_disciplina, nome, ch_semanal, periodo in disciplinas]
    else:
        return [{'id_disciplina': id_disciplina, 'nome': nome, 'ch_semanal': ch_semanal} for id_disciplina, nome, ch_semanal in disciplinas]


def obter_restricoes_professor(id_professor):
    conn = conectar()
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