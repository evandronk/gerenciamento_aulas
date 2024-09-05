
class Horario:
    def __init__(self, periodo: int, horario: list[int], dia_semana: str):
        self.periodo = periodo
        self.horario = horario  # Lista de inteiros representando as horas
        self.dia_semana = dia_semana  # Dia da semana como string

    def __repr__(self):
        return f"Horario(periodo={{self.periodo}}, horario={{self.horario}}, dia_semana={{self.dia_semana}})"


class Professor:
    def __init__(self, nome: str, id_professor: int, restricoes: list = None):
        self.nome = nome
        self.id_professor = id_professor
        self.disciplinas = []  # Lista de disciplinas associadas ao professor
        self.restricoes = restricoes if restricoes else []  # Lista de objetos Horario

    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def adicionar_restricao(self, restricao):
        self.restricoes.append(restricao)

    def __repr__(self):
        return (f"Professor(nome={self.nome}, id_professor={self.id_professor}, "
                f"disciplinas={len(self.disciplinas)}, restricoes={self.restricoes})")


class Sala:
    def __init__(self, nome: str, capacidade: int, tipo: str):
        self.nome = nome
        self.capacidade = capacidade
        self.tipo = tipo  # Tipo pode ser "laboratório" ou "sala de aula"

    def __repr__(self):
        return f"Sala(nome={{self.nome}}, capacidade={{self.capacidade}}, tipo={{self.tipo}})"


class Disciplina:
    def __init__(self, id_disciplina: str, nome: str, periodo: int, ch_semanal: int, 
                 professor: Professor = None, horario: Horario = None, sala: Sala = None):
        self.id_disciplina = id_disciplina
        self.nome = nome
        self.periodo = periodo
        self.ch_semanal = ch_semanal
        self.professor = professor
        self.nome_professor = professor.nome if professor else None
        self.horario = horario  # Horário da disciplina
        self.sala = sala  # Sala da disciplina

        if professor:
            professor.adicionar_disciplina(self)

    def __repr__(self):
        return (f"Disciplina(id_disciplina={self.id_disciplina}, nome={self.nome}, periodo={self.periodo}, "
                f"ch_semanal={self.ch_semanal}, nome_professor={self.nome_professor}, horario={self.horario}, "
                f"sala={self.sala})")



