import flet as ft
from db.professor_db import obter_professores  # Certo de onde obter os professores
from db.disciplina_db import salvar_disciplina  # Importando a função correta de salvar_disciplina

class CadastrarDisciplinaView:
    def __init__(self, main_view):
        self.main_view = main_view  # Recebe a instância de MainView
        self.nome_input = ft.TextField(label="Nome")
        self.periodo_input = ft.TextField(label="Período", keyboard_type=ft.KeyboardType.NUMBER)
        self.ch_semanal_input = ft.TextField(label="Carga Horária Semanal", keyboard_type=ft.KeyboardType.NUMBER)
        self.professor_dropdown = None
        self.professor_selecionado = None

    def build(self, page: ft.Page):
        def carregar_professores():
            """Carrega todos os professores do banco de dados."""
            professores = obter_professores()  # Função que retorna uma lista de (id, nome) dos professores
            return [ft.dropdown.Option(text=nome, key=id_prof) for id_prof, nome in professores]

        def selecionar_professor(e):
            self.professor_selecionado = self.professor_dropdown.value
            page.update()

        def validar_campos():
            """Verifica se todos os campos foram preenchidos."""
            campos_validos = True
            mensagens_erro = []

            if not self.nome_input.value.strip():
                campos_validos = False
                mensagens_erro.append("O campo Nome é obrigatório.")

            if not self.periodo_input.value.strip():
                campos_validos = False
                mensagens_erro.append("O campo Período é obrigatório.")

            if not self.ch_semanal_input.value.strip():
                campos_validos = False
                mensagens_erro.append("O campo Carga Horária Semanal é obrigatório.")

            if not self.professor_selecionado:
                campos_validos = False
                mensagens_erro.append("Selecione um Professor.")

            return campos_validos, mensagens_erro

        def salvar_disciplina_click(e):
            campos_validos, mensagens_erro = validar_campos()
            if campos_validos:
                # Salvar a disciplina no banco de dados
                salvar_disciplina(
                    id_disciplina=None,  # Se estiver usando auto-incremento, pode ser None
                    nome=self.nome_input.value.strip(),
                    periodo=int(self.periodo_input.value.strip()),
                    ch_semanal=int(self.ch_semanal_input.value.strip()),
                    id_professor=self.professor_selecionado
                )

                alerta_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text(f"A disciplina '{self.nome_input.value}' foi cadastrada com sucesso."),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo(page))],
                )
                page.dialog = alerta_sucesso
                page.dialog.open = True
            else:
                # Exibir mensagens de erro
                alerta_erro = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Column([ft.Text(msg) for msg in mensagens_erro]),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_alerta_erro(page))],
                )
                page.dialog = alerta_erro
                page.dialog.open = True

            page.update()

        self.professor_dropdown = ft.Dropdown(
            label="Selecione o Professor",
            options=carregar_professores(),
            on_change=selecionar_professor,
            width=300
        )

        salvar_btn = ft.ElevatedButton(
            text="Salvar",
            on_click=salvar_disciplina_click,
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor="#3f51b5",
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        cancelar_btn = ft.ElevatedButton(
            text="Cancelar",
            on_click=lambda e: self.main_view.limpar_area_conteudo(),
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor="#f44336",
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Cadastrar Disciplina", size=30),
                self.nome_input,
                self.periodo_input,
                self.ch_semanal_input,
                self.professor_dropdown,
                ft.Row([salvar_btn, cancelar_btn], spacing=20, alignment='center'),
            ], spacing=20),
            padding=20,
        )

    def fechar_alerta_erro(self, page):
        page.dialog.open = False
        page.update()

    def fechar_dialogo(self, page):
        page.dialog.open = False
        page.update()
        self.main_view.limpar_area_conteudo()
