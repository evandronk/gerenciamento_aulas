import sqlite3
from entities import Professor, Disciplina

def conectar():
    return sqlite3.connect('banco_dados.db')

def salvar_disciplina(id_disciplina, nome, periodo, ch_semanal, id_professor=None, horario=None, sala_nome=None):
    conn = conectar()
    cursor = conn.cursor()

    try:
        horario_periodo = horario.periodo if horario else None
        horario_horario = str(horario.horario) if horario else None
        horario_dia_semana = horario.dia_semana if horario else None

        # Inserindo a disciplina sem especificar o id_disciplina, permitindo que o banco de dados gere o ID automaticamente
        cursor.execute('''
            INSERT INTO disciplinas (nome, periodo, ch_semanal, id_professor, 
                                     horario_periodo, horario_horario, horario_dia_semana, sala_nome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, periodo, ch_semanal, id_professor,
              horario_periodo, horario_horario, horario_dia_semana, sala_nome))

        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao salvar a disciplina: {e}")
        conn.rollback()

    finally:
        conn.close()

def editar_disciplina(id_disciplina, nome=None, periodo=None, ch_semanal=None, id_professor=None, horario=None, sala_nome=None):
    conn = conectar()
    cursor = conn.cursor()

    if nome:
        cursor.execute('''
            UPDATE disciplinas
            SET nome = ?
            WHERE id_disciplina = ?
        ''', (nome, id_disciplina))

    if periodo is not None:
        cursor.execute('''
            UPDATE disciplinas
            SET periodo = ?
            WHERE id_disciplina = ?
        ''', (periodo, id_disciplina))

    if ch_semanal is not None:
        cursor.execute('''
            UPDATE disciplinas
            SET ch_semanal = ?
            WHERE id_disciplina = ?
        ''', (ch_semanal, id_disciplina))

    if id_professor is not None:
        cursor.execute('''
            UPDATE disciplinas
            SET id_professor = ?
            WHERE id_disciplina = ?
        ''', (id_professor, id_disciplina))

    if horario:
        horario_periodo = horario.periodo
        horario_horario = str(horario.horario)
        horario_dia_semana = horario.dia_semana
        cursor.execute('''
            UPDATE disciplinas
            SET horario_periodo = ?, horario_horario = ?, horario_dia_semana = ?
            WHERE id_disciplina = ?
        ''', (horario_periodo, horario_horario, horario_dia_semana, id_disciplina))

    if sala_nome is not None:
        cursor.execute('''
            UPDATE disciplinas
            SET sala_nome = ?
            WHERE id_disciplina = ?
        ''', (sala_nome, id_disciplina))

    conn.commit()
    conn.close()

def excluir_disciplina(id_disciplina):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM disciplinas WHERE id_disciplina = ?
    ''', (id_disciplina,))

    conn.commit()
    conn.close()

def obter_disciplinas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id_disciplina, periodo, nome, ch_semanal, id_professor
        FROM disciplinas
        ORDER BY periodo, nome
    ''')
    disciplinas = cursor.fetchall()

    conn.close()
    return disciplinas

def obter_professores():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id_professor, nome
        FROM professores
        ORDER BY nome
    ''')
    professores = cursor.fetchall()

    conn.close()
    return professores


def obter_disciplinas_com_horarios():
    conn = conectar()
    cursor = conn.cursor()

    # Buscar todas as disciplinas com seus horários diretamente da tabela `disciplinas`
    cursor.execute('''
        SELECT periodo, nome, ch_semanal, horario_periodo, horario_horario, horario_dia_semana 
        FROM disciplinas
    ''')

    disciplinas_dados = cursor.fetchall()

    disciplinas = []
    for periodo, nome_disciplina, ch_semanal, horario_periodo, horario_horario, horario_dia_semana in disciplinas_dados:
        horarios = []
        if horario_horario:
            horarios.append({
                'periodo': horario_periodo,
                'horario': horario_horario,
                'dia_semana': horario_dia_semana
            })

        disciplina = {
            'periodo': periodo,
            'nome': nome_disciplina,
            'ch_semanal': ch_semanal,
            'horarios': horarios
        }

        disciplinas.append(disciplina)

    conn.close()

    return disciplinas



