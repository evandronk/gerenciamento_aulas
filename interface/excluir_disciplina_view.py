import flet as ft
from db.disciplina_db import obter_disciplinas, excluir_disciplina
from db.professor_db import obter_professores

class ExcluirDisciplinaView:
    def __init__(self, main_view):
        self.main_view = main_view
        self.disciplinas_map = {}  # Dicionário para mapear texto do dropdown para disciplina
        self.disciplinas = []  # Lista para armazenar as disciplinas carregadas
        self.professores_map = {}  # Dicionário para mapear ID do professor para nome
        self.nome_input = ft.TextField(label="Nome", read_only=True)
        self.periodo_input = ft.TextField(label="Período", read_only=True)
        self.ch_semanal_input = ft.TextField(label="Carga Horária Semanal", read_only=True)
        self.professor_input = ft.TextField(label="Professor", read_only=True)

    def build(self, page: ft.Page):
        def carregar_disciplinas():
            """Carrega todas as disciplinas do banco de dados."""
            self.disciplinas = obter_disciplinas()
            for disciplina in self.disciplinas:
                display_text = f"Período: {disciplina[1]} - {disciplina[2]}"
                self.disciplinas_map[display_text] = disciplina
            return [
                ft.dropdown.Option(
                    text=display_text,
                    key=display_text  # Usar a string de exibição como chave
                ) for display_text in self.disciplinas_map
            ]

        def carregar_professores():
            """Carrega todos os professores do banco de dados e cria um mapa de ID para nome."""
            professores = obter_professores()
            self.professores_map = {id_prof: nome for id_prof, nome in sorted(professores, key=lambda p: p[1])}
            # Não é mais necessário criar um dropdown para professores, pois é apenas para visualização
            return []

        def selecionar_disciplina(e):
            """Carrega os dados da disciplina selecionada nos campos de exibição."""
            disciplina_selecionada_texto = dropdown_disciplina.value  # Isso é a string do dropdown
            disciplina = self.disciplinas_map.get(disciplina_selecionada_texto)  # Mapeia para a disciplina completa

            if disciplina:
                # Preenche os TextFields com os dados da disciplina
                self.nome_input.value = disciplina[2]
                self.periodo_input.value = str(disciplina[1])
                self.ch_semanal_input.value = str(disciplina[3])

                # Exibe o nome do professor ao invés do ID
                professor_id = disciplina[4]
                self.professor_input.value = self.professores_map.get(professor_id, "")

                page.update()

        def excluir_disciplina_click(e):
            """Exclui a disciplina selecionada."""
            disciplina_selecionada_texto = dropdown_disciplina.value
            disciplina = self.disciplinas_map.get(disciplina_selecionada_texto)

            if disciplina:
                excluir_disciplina(id_disciplina=disciplina[0])  # Usar o id_disciplina da disciplina mapeada

                # Exibe mensagem de sucesso
                alerta_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text(f"A disciplina '{self.nome_input.value}' foi excluída com sucesso."),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo(page))],
                )
                page.dialog = alerta_sucesso
                page.dialog.open = True

            page.update()

        dropdown_disciplina = ft.Dropdown(
            label="Selecione a Disciplina",
            options=carregar_disciplinas(),
            on_change=selecionar_disciplina,
            width=500,
        )

        # Carregar os professores ao construir a página
        carregar_professores()

        excluir_btn = ft.ElevatedButton(
            text="Excluir",
            on_click=excluir_disciplina_click,
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor="#f44336",
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
                bgcolor="#3f51b5",
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Excluir Disciplina", size=30),
                dropdown_disciplina,
                self.nome_input,
                self.periodo_input,
                self.ch_semanal_input,
                self.professor_input,
                ft.Row([excluir_btn, cancelar_btn], spacing=20, alignment='center'),
            ], spacing=20),
            padding=20,
        )

    def fechar_dialogo(self, page):
        page.dialog.open = False
        page.update()
        self.main_view.limpar_area_conteudo()
