import flet as ft
from db.professor_db import obter_professores_com_disciplinas


class RelatorioProfessoresView:
    def __init__(self, main_view):
        self.main_view = main_view

    def build(self, page: ft.Page):
        def carregar_relatorio():
            """Carrega os dados de professores e suas disciplinas."""
            professores = obter_professores_com_disciplinas()
            items = []

            for professor in professores:
                nome = professor['nome']
                disciplinas = professor['disciplinas']

                carga_horaria = sum(d['ch_semanal'] for d in disciplinas)
                disciplinas_texto = "\n".join(
                    [f"Período: {d['periodo']} - {d['nome']} ({d['ch_semanal']}h)" for d in disciplinas])

                items.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(nome)),
                        ft.DataCell(ft.Text(str(carga_horaria))),
                        ft.DataCell(ft.Text(disciplinas_texto))
                    ]
                ))

            return items

        # Criação da ListView para exibir os professores
        list_view = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nome")),
                ft.DataColumn(label=ft.Text("Carga Horária (Aulas)")),
                ft.DataColumn(label=ft.Text("Disciplinas")),
            ],
            rows=carregar_relatorio()
        )

        # Layout principal
        return ft.Container(
            content=ft.Column([
                ft.Text("Relatório de Professores", size=30),
                list_view,
                ft.ElevatedButton(
                    text="Fechar",
                    on_click=lambda e: self.main_view.limpar_area_conteudo(),
                    width=150,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor="#f44336",
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ], spacing=20),
            padding=20,
        )
