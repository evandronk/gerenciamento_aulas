import flet as ft
from db.horario_db import obter_periodos_disponiveis, obter_disciplinas_por_periodo, salvar_horario
from db.professor_db import obter_professores_com_disciplinas


class HorarioManualView:
    def __init__(self, main_view):
        self.main_view = main_view
        self.matriz_disciplinas = {}
        self.professor_horarios = {}
        self.dropdown_matrix = {}
        self.checkboxes_matriz = {}
        self.rows_matrix = {}
        self.lista_periodos = []

    def build(self, page: ft.Page):
        # Inicialize os horários para diferentes períodos
        horarios_manha = ["07:30 - 08:20", "08:20 - 09:10", "09:10 - 10:00", "10:20 - 11:10", "11:10 - 12:00",
                          "12:00 - 12:50"]
        horarios_tarde = ["13:00 - 13:50", "13:50 - 14:40", "14:40 - 15:30", "15:50 - 16:40", "16:40 - 17:30",
                          "17:30 - 18:20"]
        horarios_noite = ["19:00 - 19:45", "19:45 - 20:30", "20:30 - 21:15", "21:25 - 22:10", "22:10 - 22:55"]

        def inicializar_matriz():
            # Limpa a lista de períodos
            self.lista_periodos = []

            # Obtém os períodos disponíveis a partir das disciplinas cadastradas
            disciplinas = obter_disciplinas_por_periodo(None)  # Obtém todas as disciplinas sem filtro por período

            # Verifica se as disciplinas foram carregadas corretamente
            print(f"Disciplinas carregadas: {disciplinas}")

            # Cria a lista de períodos sem duplicatas
            for d in disciplinas:
                periodo = d['periodo']
                if periodo not in self.lista_periodos:
                    self.lista_periodos.append(periodo)

            # Verifica se os períodos foram extraídos corretamente
            print(f"Lista de períodos: {self.lista_periodos}")

            professores_disciplinas = obter_professores_com_disciplinas()

            for periodo in self.lista_periodos:
                self.matriz_disciplinas[periodo] = {}
                self.dropdown_matrix[periodo] = []
                self.rows_matrix[periodo] = []
                self.checkboxes_matriz[periodo] = {
                    'manha': ft.Checkbox(label="Manhã", value=True,
                                         on_change=lambda e: atualizar_visibilidade(periodo)),
                    'tarde': ft.Checkbox(label="Tarde", value=True,
                                         on_change=lambda e: atualizar_visibilidade(periodo)),
                    'noite': ft.Checkbox(label="Noite", value=True, on_change=lambda e: atualizar_visibilidade(periodo))
                }
                disciplinas_periodo = [d for d in disciplinas if d['periodo'] == periodo]

                for d in disciplinas_periodo:
                    nome_professor = None
                    for professor in professores_disciplinas:
                        for disciplina in professor['disciplinas']:
                            if disciplina['nome'] == d['nome']:
                                nome_professor = professor['nome']
                                break

                    # Armazena o id da disciplina corretamente
                    self.matriz_disciplinas[periodo][d['id_disciplina']] = {  # Armazenamos o ID como chave
                        'nome': d['nome'],  # Nome da disciplina agora está nos dados
                        'professor': nome_professor,
                        'horarios': [],
                        'ch_semanal': d['ch_semanal']
                    }

                    if nome_professor not in self.professor_horarios:
                        self.professor_horarios[nome_professor] = []

        def atualizar_visibilidade(periodo):
            """Atualiza a visibilidade dos horários com base nos checkboxes."""
            visible_horarios = []

            # Cria uma lista com os horários visíveis
            if self.checkboxes_matriz[periodo]['manha'].value:
                visible_horarios.extend(horarios_manha)
            if self.checkboxes_matriz[periodo]['tarde'].value:
                visible_horarios.extend(horarios_tarde)
            if self.checkboxes_matriz[periodo]['noite'].value:
                visible_horarios.extend(horarios_noite)

            for idx, horario in enumerate(horarios_manha + horarios_tarde + horarios_noite):
                row = self.rows_matrix[periodo][idx]
                if horario in visible_horarios:
                    row.visible = True
                else:
                    row.visible = False
                row.update()

        def atualizar_selecao(e, horario, dia_semana, periodo):
            valor_selecionado = int(e.control.value) if e.control.value != " " else " "
            disciplina_anterior = e.control.data.get('disciplina_anterior', None)

            # Remove a disciplina anterior do horário, se houver
            if disciplina_anterior:
                self.matriz_disciplinas[periodo][disciplina_anterior]['horarios'].remove((horario, dia_semana))
                professor_anterior = self.matriz_disciplinas[periodo][disciplina_anterior]['professor']
                self.professor_horarios[professor_anterior].remove((horario, dia_semana))
                print(f"{disciplina_anterior} removida do horário {horario}, {dia_semana}")

            # Se o valor selecionado for "vazio", não tenta buscar na matriz de disciplinas e libera o professor
            if valor_selecionado is None or valor_selecionado == " ":
                e.control.data['disciplina_anterior'] = None
                print(f"Horário {horario}, {dia_semana} agora está vazio.")
            else:
                # Encontra a disciplina pelo ID (valor_selecionado)
                dados_disciplina = self.matriz_disciplinas[periodo].get(valor_selecionado)
                if dados_disciplina is None:
                    print(f"Disciplina com ID {valor_selecionado} não encontrada!")
                    return

                professor = dados_disciplina['professor']

                # Verifica se o professor já tem um compromisso nesse horário
                if horario_conflitante(professor, horario, dia_semana):
                    e.control.value = None  # Reverte a seleção
                    print(f"Conflito de horário para {professor} no horário {horario}. Seleção cancelada.")
                else:
                    # Verifica se a carga horária já foi atingida
                    ch_usada = len(dados_disciplina['horarios'])
                    ch_total = dados_disciplina['ch_semanal']

                    if ch_usada < ch_total:
                        # Atualiza as matrizes
                        dados_disciplina['horarios'].append((horario, dia_semana))
                        self.professor_horarios[professor].append((horario, dia_semana))
                        e.control.data['disciplina_anterior'] = valor_selecionado
                        print(f"{dados_disciplina['nome']} alocado para {professor} no horário {horario}, {dia_semana}.")
                    else:
                        e.control.value = None  # Reverte a seleção
                        print(f"{dados_disciplina['nome']} já atingiu a carga horária máxima. Seleção cancelada.")

            # Atualiza os dropdowns após a mudança
            for periodo in self.lista_periodos:
                atualizar_dropdowns(periodo)
            e.control.update()
            page.update()

        def atualizar_dropdowns(periodo):
            """Atualiza o estado dos dropdowns com base nas restrições atuais."""
            for row_dropdowns in self.dropdown_matrix[periodo]:
                for dropdown in row_dropdowns:
                    horario = dropdown.data['horario']
                    dia_semana = dropdown.data['dia_semana']

                    # Adiciona a opção vazia para permitir deseleção
                    dropdown.options = [ft.dropdown.Option(key=" ", text=" ")]  # Opção vazia no início

                    # Preenche as opções com disciplinas disponíveis ou indisponíveis
                    dropdown.options += [
                        ft.dropdown.Option(
                            text=f"{dados['nome'][:25]}." if len(dados['nome']) > 25 else dados['nome'],
                            key=id_disciplina,  # Usamos o ID da disciplina como a key
                            disabled=(len(dados['horarios']) >= dados['ch_semanal'] or horario_conflitante(
                                dados['professor'], horario, dia_semana))
                        ) for id_disciplina, dados in self.matriz_disciplinas[periodo].items()  # id_disciplina é a chave
                    ]

                    dropdown.update()

        def horario_conflitante(professor, horario, dia_semana):
            """Verifica se o professor já tem uma aula no mesmo horário e dia da semana."""
            return (horario, dia_semana) in self.professor_horarios.get(professor, [])

        def criar_dropdown(horario, dia_semana, periodo):
            # Cria dropdown para cada célula de horário
            dropdown = ft.Dropdown(
                expand=False,
                height=40,
                text_size=12,
                width=200,
                on_change=lambda e: atualizar_selecao(e, horario, dia_semana, periodo)
            )
            dropdown.data = {"horario": horario, "dia_semana": dia_semana}  # Adiciona dados para referência futura
            dropdown.options = [
                ft.dropdown.Option(
                    text=f"{dados['nome'][:25]}." if len(dados['nome']) > 25 else dados['nome'],  # Nome abreviado
                    key=id_disciplina,  # O ID da disciplina está em id_disciplina
                    disabled=(len(dados['horarios']) >= dados['ch_semanal'] or horario_conflitante(dados['professor'],
                                                                                                   horario, dia_semana))
                ) for id_disciplina, dados in self.matriz_disciplinas[periodo].items()
            ]
            return dropdown

        def criar_aba_periodo(periodo):
            checkboxes = ft.Row(
                controls=[
                    self.checkboxes_matriz[periodo]['manha'],
                    self.checkboxes_matriz[periodo]['tarde'],
                    self.checkboxes_matriz[periodo]['noite']
                ],
                spacing=20,
            )

            rows_column = ft.Column(scroll='auto', expand=True)
            horarios_selecionados = horarios_manha + horarios_tarde + horarios_noite

            # Adiciona os dias da semana no topo
            dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            dias_row = ft.Row(
                controls=[ft.Text("", width=100)] +  # Primeiro espaço vazio para alinhar com horários
                         [ft.Text(dia, width=200, text_align=ft.TextAlign.CENTER) for dia in dias_da_semana],
                spacing=10,
            )
            rows_column.controls.append(dias_row)  # Adiciona a linha com os dias da semana no topo

            # Cria o primeiro bloco (manhã)
            for horario in horarios_manha:
                row_dropdowns = [
                    criar_dropdown(horario, dia, periodo)
                    for dia in dias_da_semana  # Mantém o mesmo array de dias da semana
                ]
                row = ft.Row(
                    [ft.Text(horario, width=100)] + row_dropdowns,
                    spacing=10,
                    visible=True,  # Todos começam visíveis, a visibilidade será controlada pelos checkboxes
                )
                if row is not None:  # Verificação adicional
                    rows_column.controls.append(row)
                    self.dropdown_matrix[periodo].append(row_dropdowns)
                    self.rows_matrix[periodo].append(row)

            # Adiciona a divisão entre manhã e tarde
            rows_column.controls.append(ft.Divider(height=1, color=ft.colors.GREY_500))

            # Cria o segundo bloco (tarde)
            for horario in horarios_tarde:
                row_dropdowns = [
                    criar_dropdown(horario, dia, periodo)
                    for dia in dias_da_semana
                ]
                row = ft.Row(
                    [ft.Text(horario, width=100)] + row_dropdowns,
                    spacing=10,
                    visible=True,  # Todos começam visíveis, a visibilidade será controlada pelos checkboxes
                )
                if row is not None:  # Verificação adicional
                    rows_column.controls.append(row)
                    self.dropdown_matrix[periodo].append(row_dropdowns)
                    self.rows_matrix[periodo].append(row)

            # Adiciona a divisão entre tarde e noite
            rows_column.controls.append(ft.Divider(height=1, color=ft.colors.GREY_500))

            # Cria o terceiro bloco (noite)
            for horario in horarios_noite:
                row_dropdowns = [
                    criar_dropdown(horario, dia, periodo)
                    for dia in dias_da_semana
                ]
                row = ft.Row(
                    [ft.Text(horario, width=100)] + row_dropdowns,
                    spacing=10,
                    visible=True,  # Todos começam visíveis, a visibilidade será controlada pelos checkboxes
                )
                if row is not None:  # Verificação adicional
                    rows_column.controls.append(row)
                    self.dropdown_matrix[periodo].append(row_dropdowns)
                    self.rows_matrix[periodo].append(row)

            rows_column.controls.append(ft.Container(height=20))
            rows_column.scroll = ft.ScrollMode.ALWAYS

            return ft.Tab(
                text=f"{periodo}° Período",
                content=ft.Container(
                    content=ft.Column([ft.Container(height=2), checkboxes, ft.Container(height=2),
                                       ft.Row([ft.Container(content=rows_column)], expand=True,
                                              scroll=ft.ScrollMode.ALWAYS), ft.Container(height=2)], expand=True),
                    expand=False,
                )
            )

        inicializar_matriz()
        self.lista_periodos.sort()
        tabs = [criar_aba_periodo(periodo) for periodo in self.lista_periodos]

        # Verifica se as abas estão sendo criadas corretamente
        print(f"Abas criadas: {len(tabs)}")


        def salvar_alteracoes():
            # Iterar sobre cada período
            for periodo in self.lista_periodos:
                # Iterar sobre as linhas de horários e os dias da semana (cada dropdown de horários)
                for row_dropdowns in self.dropdown_matrix[periodo]:
                    for dropdown in row_dropdowns:
                        horario = dropdown.data['horario']
                        dia_semana = dropdown.data['dia_semana']
                        valor_selecionado = int(dropdown.value) if (dropdown.value != " " and dropdown.value is not None) else None  # Valor selecionado no dropdown (ID da disciplina)

                        if valor_selecionado and valor_selecionado != " ":  # Verifica se o valor é válido
                            # Encontrar os dados da disciplina selecionada
                            dados_disciplina = self.matriz_disciplinas[periodo].get(valor_selecionado)

                            if dados_disciplina is not None:
                                professor = dados_disciplina['professor']

                                # Verifica se o professor já tem um compromisso nesse horário
                                print(horario_conflitante(professor, horario, dia_semana))
                                if not horario_conflitante(professor, horario, dia_semana):
                                    # Adiciona o horário à disciplina e professor
                                    dados_disciplina['horarios'].append((horario, dia_semana))
                                    self.professor_horarios[professor].append((horario, dia_semana))
                                    print('professor')
                                    # Salva o horário no banco de dados
                                    salvar_horario(periodo, horario, dia_semana)
                                    print(
                                        f"Salvo: {dados_disciplina['nome']} no período {periodo} para {professor} em {horario}, {dia_semana}.")
                                else: print('erro')


            print("Alterações salvas com sucesso.")

        salvar_button = ft.ElevatedButton(text="Salvar Alterações", on_click=lambda e: salvar_alteracoes())

        return ft.Container(
            content=ft.Column([
                ft.Tabs(
                    tabs=tabs,
                    expand=True,
                    scrollable=True,
                ),
                salvar_button
            ]),
            padding=ft.padding.all(10),
            expand=True
        )




