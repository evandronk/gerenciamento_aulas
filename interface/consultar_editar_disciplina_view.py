import flet as ft
from db.disciplina_db import obter_disciplinas, editar_disciplina
from db.professor_db import obter_professores


class ConsultarEditarDisciplinaView:
    def __init__(self, main_view):
        self.main_view = main_view
        self.disciplinas_map = {}  # Dicionário para mapear texto do dropdown para disciplina
        self.disciplinas = []  # Lista para armazenar as disciplinas carregadas
        self.nome_input = ft.TextField(label="Nome")
        self.periodo_input = ft.TextField(label="Período", keyboard_type=ft.KeyboardType.NUMBER)
        self.ch_semanal_input = ft.TextField(label="Carga Horária Semanal", keyboard_type=ft.KeyboardType.NUMBER)
        self.professor_dropdown = None

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
            """Carrega todos os professores do banco de dados."""
            professores = obter_professores()
            return [ft.dropdown.Option(text=nome, key=id_prof) for id_prof, nome in
                    sorted(professores, key=lambda p: p[1])]

        def selecionar_disciplina(e):
            """Carrega os dados da disciplina selecionada nos campos de edição."""
            disciplina_selecionada_texto = dropdown_disciplina.value  # Isso é a string do dropdown
            disciplina = self.disciplinas_map.get(disciplina_selecionada_texto)  # Mapeia para a disciplina completa

            if disciplina:
                # Preenche os TextFields com os dados da disciplina
                self.nome_input.value = disciplina[2]
                self.periodo_input.value = str(disciplina[1])
                self.ch_semanal_input.value = str(disciplina[3])

                # Habilitar o dropdown de professores e selecionar o professor associado
                self.professor_dropdown.disabled = False
                self.professor_dropdown.value = disciplina[4]

                page.update()

        def validar_campos():
            """Verifica se todos os campos foram preenchidos corretamente."""
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

            if not self.professor_dropdown.value:
                campos_validos = False
                mensagens_erro.append("Selecione um Professor.")

            return campos_validos, mensagens_erro

        def salvar_disciplina_click(e):
            """Salva as alterações feitas na disciplina."""
            campos_validos, mensagens_erro = validar_campos()
            if campos_validos:
                # Recupera a disciplina selecionada pelo texto exibido
                disciplina_selecionada_texto = dropdown_disciplina.value
                disciplina = self.disciplinas_map.get(disciplina_selecionada_texto)
                print(disciplina)
                # Atualiza a disciplina com os dados dos TextFields
                editar_disciplina(
                    id_disciplina=disciplina[0],  # Usar o id_disciplina da disciplina mapeada
                    nome=self.nome_input.value.strip(),
                    periodo=int(self.periodo_input.value.strip()),
                    ch_semanal=int(self.ch_semanal_input.value.strip()),
                    id_professor=self.professor_dropdown.value
                )
                print(disciplina[0])
                print(self.nome_input.value.strip())
                # Exibe mensagem de sucesso
                alerta_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text(f"A disciplina '{self.nome_input.value}' foi atualizada com sucesso."),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo(page))],
                )
                page.dialog = alerta_sucesso
                page.dialog.open = True
            else:
                # Exibe mensagens de erro
                alerta_erro = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Column([ft.Text(msg) for msg in mensagens_erro]),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_alerta_erro(page))],
                )
                page.dialog = alerta_erro
                page.dialog.open = True

            page.update()

        dropdown_disciplina = ft.Dropdown(
            label="Selecione a Disciplina",
            options=carregar_disciplinas(),
            on_change=selecionar_disciplina,
            width=500,

        )

        self.professor_dropdown = ft.Dropdown(
            label="Selecione o Professor",
            options=carregar_professores(),
            width=300,
            disabled=True  # Inicialmente desabilitado
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
                ft.Text("Consultar/Editar Disciplina", size=30),
                dropdown_disciplina,
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
