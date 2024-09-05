import flet as ft
from entities import Horario
from db.professor_db import obter_professores, obter_restricoes_professor, salvar_restricoes_professor

class ConsultarEditarProfessorView:
    def __init__(self, main_view):
        self.main_view = main_view  # Recebe a instância de MainView
        self.restricoes = []  # Lista de restrições que serão adicionadas
        self.dropdown_map = {}  # Mapeia cada dia da semana para seu dropdown
        self.ordem_dias = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"]  # Ordem dos dias
        self.professor_selecionado = None  # Professor selecionado no dropdown

    def build(self, page: ft.Page):
        def carregar_professores():
            """Carrega todos os professores do banco de dados."""
            professores = obter_professores()  # Função que retorna uma lista de (id, nome) dos professores
            return [ft.dropdown.Option(text=nome, key=id_prof) for id_prof, nome in professores]

        def carregar_restricoes_professor(id_professor):
            """Carrega as restrições do professor selecionado."""
            self.restricoes = obter_restricoes_professor(id_professor)  # Retorna lista de (dia_semana, horario)
            atualizar_dropdowns()
            atualizar_restricoes_lista()

        def selecionar_professor(e):
            self.professor_selecionado = dropdown_professor.value
            carregar_restricoes_professor(self.professor_selecionado)
            page.update()

        dropdown_professor = ft.Dropdown(
            label="Selecione o Professor",
            options=carregar_professores(),
            on_change=selecionar_professor,
            width=300
        )

        def atualizar_dropdowns():
            """Atualiza o estado dos dropdowns com base nas restrições atuais."""
            restricoes_por_dia = {dia: [] for dia in self.ordem_dias}
            for dia_semana, horario in self.restricoes:
                # Remover colchetes e aspas dos horários
                horario = horario.strip("[]").strip("'").strip('"')
                restricoes_por_dia[dia_semana].append(horario)

            for dia, dropdown in self.dropdown_map.items():
                dropdown.options = [
                    ft.dropdown.Option(
                        text=f"{h} (Indisponível)" if h in restricoes_por_dia[dia] else h,
                        key=h,
                        disabled=h in restricoes_por_dia[dia]
                    ) for h in dropdown.original_options
                ]
                dropdown.update()

        def adicionar_restricao(e, dia_semana, dropdown):
            horario_selecionado = dropdown.value
            if horario_selecionado:
                self.restricoes.append((dia_semana, horario_selecionado))

                # Ordena as restrições adicionadas
                self.restricoes.sort(key=lambda x: (self.ordem_dias.index(x[0]), x[1]))

                # Atualiza a lista de restrições adicionadas
                atualizar_restricoes_lista()

                # Atualiza todos os dropdowns
                atualizar_dropdowns()

                dropdown.value = None  # Reseta o dropdown
                page.update()

        def remover_restricao(e, dia_semana, horario_selecionado):
            # Remove a restrição da lista
            self.restricoes = [(d, h) for d, h in self.restricoes if not (d == dia_semana and h == horario_selecionado)]
            atualizar_restricoes_lista()

            # Atualiza todos os dropdowns
            atualizar_dropdowns()

            page.update()

        def atualizar_restricoes_lista():
            restricoes_lista.controls.clear()

            for d, h in self.restricoes:
                # Formatar a exibição das restrições removendo colchetes e aspas
                horario_formatado = h.strip("[]").strip("'").strip('"')
                restricoes_lista.controls.append(
                    ft.Row([
                        ft.Text(f"{d}: {horario_formatado}"),
                        ft.IconButton(
                            icon=ft.icons.REMOVE,
                            on_click=lambda e, dia=d, hora=horario_formatado: remover_restricao(e, dia, hora)
                        )
                    ], alignment='start')
                )

        def salvar_restricoes(e):
            if self.professor_selecionado:
                lista_restricoes = [
                    Horario(periodo=0, horario=[horario], dia_semana=dia)
                    for dia, horario in self.restricoes
                ] if self.restricoes else None

                salvar_restricoes_professor(self.professor_selecionado, lista_restricoes)

                alerta_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text(f"Restrições do professor foram salvas com sucesso."),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo(page))],
                )
                page.dialog = alerta_sucesso
                page.dialog.open = True
                page.update()

        def cancelar(e):
            self.main_view.limpar_area_conteudo()

        salvar_btn = ft.ElevatedButton(
            text="Salvar",
            on_click=salvar_restricoes,
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Cor do texto
                bgcolor="#3f51b5",  # Cor de fundo primária
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        cancelar_btn = ft.ElevatedButton(
            text="Cancelar",
            on_click=cancelar,
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Cor do texto
                bgcolor="#f44336",  # Cor de fundo secundária
                elevation=4,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        # Lista de horários possíveis (simulando o que estaria no banco de dados)
        horarios_possiveis = [
            "07:30 - 08:20", "08:20 - 09:10", "09:10 - 10:00",
            "10:20 - 11:10", "11:10 - 12:00", "12:00 - 12:50",
            "13:50 - 14:40", "14:40 - 15:30", "15:30 - 16:20",
            "16:40 - 17:30", "17:30 - 18:20"
        ]

        # Criando dropdowns para cada dia da semana
        dropdowns = []
        dias_semana = self.ordem_dias
        for dia in dias_semana:
            original_options = list(horarios_possiveis)
            dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(text=h, key=h) for h in original_options],
                width=250
            )
            self.dropdown_map[dia] = dropdown
            dropdown.original_options = original_options  # Armazena as opções originais

            adicionar_btn = ft.IconButton(
                icon=ft.icons.ADD,
                on_click=lambda e, d=dia, dd=dropdown: adicionar_restricao(e, d, dd)
            )
            dropdowns.append(ft.Row([ft.Text(dia, width=120), dropdown, adicionar_btn], alignment='start'))

        # Definindo altura fixa para ambas as colunas
        altura_colunas = 400  # Definindo uma altura fixa para as colunas

        restricoes_lista = ft.ListView([], auto_scroll=True, expand=True)

        return ft.Container(
            content=ft.Column([
                ft.Text("Consultar/Editar Professor", size=30),
                dropdown_professor,
                ft.Row(
                    [
                        # Coluna de dropdowns
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text("Restrições", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Column(dropdowns, spacing=10, alignment='start'),
                                ],
                                expand=True,
                                alignment='start'
                            ),
                            height=altura_colunas,  # Altura fixa para a coluna da esquerda
                        ),
                        # Coluna de restrições adicionadas
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text("Restrições Adicionadas:", size=20, weight=ft.FontWeight.BOLD),
                                    restricoes_lista,
                                ],
                                expand=True,
                                alignment='start'
                            ),
                            height=altura_colunas,  # Altura fixa para a coluna da direita
                            width=300,  # Largura fixa para a coluna da direita
                            padding=ft.padding.only(left=20)
                        ),
                    ],
                    spacing=20,
                    alignment='start',
                    vertical_alignment='start'  # Garante que ambas as colunas comecem no mesmo nível
                ),
                ft.Row([salvar_btn, cancelar_btn], spacing=20, alignment='center'),
            ], spacing=20),
            padding=20,
        )

    def fechar_dialogo(self, page):
        page.dialog.open = False
        page.update()
        self.main_view.limpar_area_conteudo()

