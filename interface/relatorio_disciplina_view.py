import flet as ft
from db.disciplina_db import obter_disciplinas_com_horarios


class RelatorioDisciplinaView:
    def __init__(self, main_view):
        self.main_view = main_view
        self.ordenacao_atual = "periodo"

    def build(self, page: ft.Page):
        def carregar_relatorio():
            """Carrega os dados de disciplinas e seus horários."""
            disciplinas = obter_disciplinas_com_horarios()

            # Ordena as disciplinas com base na ordenação atual
            if self.ordenacao_atual == "periodo":
                disciplinas.sort(key=lambda d: d['periodo'])
            elif self.ordenacao_atual == "nome":
                disciplinas.sort(key=lambda d: d['nome'])

            items = []
            for disciplina in disciplinas:
                nome = disciplina['nome']
                periodo = disciplina['periodo']
                ch_semanal = disciplina['ch_semanal']

                # Limita o número de horários à carga horária semanal
                horarios_texto = "\n".join([
                    f"{h['dia_semana']} - {h['horario']}"
                    for h in disciplina['horarios'][:ch_semanal]
                ])

                items.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(periodo))),
                        ft.DataCell(ft.Text(nome)),
                        ft.DataCell(ft.Text(str(ch_semanal))),
                        ft.DataCell(ft.Text(horarios_texto)),
                    ]
                ))

            return items

        def ordenar_por_periodo(e):
            self.ordenacao_atual = "periodo"
            list_view.rows = carregar_relatorio()
            page.update()

        def ordenar_por_nome(e):
            self.ordenacao_atual = "nome"
            list_view.rows = carregar_relatorio()
            page.update()

        # Criação da ListView para exibir as disciplinas
        list_view = ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.TextButton("Período", on_click=ordenar_por_periodo)
                ),
                ft.DataColumn(
                    label=ft.TextButton("Nome da Disciplina", on_click=ordenar_por_nome)
                ),
                ft.DataColumn(label=ft.Text("Carga Horária (h)")),
                ft.DataColumn(label=ft.Text("Horários")),
            ],
            rows=carregar_relatorio()
        )

        # Layout principal
        return ft.Container(
            content=ft.Column([
                ft.Text("Relatório de Disciplinas", size=30),
                list_view,
                ft.ElevatedButton(
                    text="Voltar",
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
