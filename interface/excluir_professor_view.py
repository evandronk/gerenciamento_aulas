import flet as ft
from db.professor_db import obter_professores, excluir_professor_com_restricoes

class ExcluirProfessorView:
    def __init__(self, main_view):
        self.main_view = main_view  # Recebe a instância de MainView
        self.professor_selecionado = None  # Professor selecionado no dropdown

    def build(self, page: ft.Page):
        def carregar_professores():
            """Carrega todos os professores do banco de dados."""
            professores = obter_professores()  # Função que retorna uma lista de (id, nome) dos professores
            return [ft.dropdown.Option(text=nome, key=id_prof) for id_prof, nome in professores]

        def selecionar_professor(e):
            self.professor_selecionado = dropdown_professor.value
            page.update()

        def excluir_professor(e):
            if self.professor_selecionado:
                excluir_professor_com_restricoes(self.professor_selecionado)

                alerta_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text(f"O Professor foi excluído com sucesso."),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo(page))],
                )
                page.dialog = alerta_sucesso
                page.dialog.open = True
                page.update()

        dropdown_professor = ft.Dropdown(
            label="Selecione o Professor",
            options=carregar_professores(),
            on_change=selecionar_professor,
            width=300
        )

        excluir_btn = ft.ElevatedButton(
            text="Excluir",
            on_click=excluir_professor,
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Cor do texto
                bgcolor="#f44336",  # Cor de fundo de exclusão (vermelho)
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        cancelar_btn = ft.ElevatedButton(
            text="Cancelar",
            on_click=lambda e: self.main_view.limpar_area_conteudo(),
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Cor do texto
                bgcolor="#3f51b5",  # Cor de fundo primária (azul)
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Excluir Professor", size=30),
                dropdown_professor,
                ft.Row([excluir_btn, cancelar_btn], spacing=20, alignment='center'),
            ], spacing=20),
            padding=20,
        )

    def fechar_dialogo(self, page):
        page.dialog.open = False
        page.update()
        self.main_view.limpar_area_conteudo()
