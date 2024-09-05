import flet as ft
from interface.cadastrar_professor_view import CadastrarProfessorView
from interface.consultar_editar_professor_view import ConsultarEditarProfessorView
from interface.excluir_professor_view import ExcluirProfessorView
from interface.cadastrar_disciplina_view import CadastrarDisciplinaView
from interface.consultar_editar_disciplina_view import ConsultarEditarDisciplinaView
from interface.excluir_disciplina_view import ExcluirDisciplinaView
from interface.relatorio_disciplina_view import RelatorioDisciplinaView
from interface.horario_manual_view import HorarioManualView
from interface.exportar_horario_view import ExportarHorarioView
from interface.cadastrar_sala_view import CadastrarSalaView
from interface.consultar_editar_sala_view import ConsultarEditarSalaView
from interface.relatorio_sala_view import RelatorioSalaView
from interface.relatorio_professor_view import RelatorioProfessoresView  # Importação da nova view

class MainView:
    def __init__(self):
        self.submenu_aberto = None
        self.content_area = None

    def run(self):
        ft.app(target=self.build)

    def build(self, page: ft.Page):
        #page.theme = ft.Theme(color_scheme_seed="grey")
        page.title = "Distribuição de Aulas"
        page.bgcolor = ft.colors.WHITE
        page.padding = 0

        def toggle_submenu(e, submenu):
            if self.submenu_aberto and self.submenu_aberto != submenu:
                self.submenu_aberto.visible = False

            submenu.visible = not submenu.visible
            self.submenu_aberto = submenu if submenu.visible else None
            page.update()

        def load_content(content_func):
            self.content_area.controls.clear()
            self.content_area.controls.append(content_func(page))
            page.update()

        # Funções para carregar as telas
        def open_cadastrar_professor(page):
            load_content(CadastrarProfessorView(main_view=self).build)

        def open_consultar_editar_professor(page):
            load_content(ConsultarEditarProfessorView(main_view=self).build)

        def open_excluir_professor(page):
            load_content(ExcluirProfessorView(main_view=self).build)

        def open_cadastrar_disciplina(page):
            load_content(CadastrarDisciplinaView(main_view=self).build)

        def open_consultar_editar_disciplina(page):
            load_content(ConsultarEditarDisciplinaView(main_view=self).build)

        def open_excluir_disciplina(page):
            load_content(ExcluirDisciplinaView(main_view=self).build)

        def open_relatorio_disciplina(page):
            load_content(RelatorioDisciplinaView(main_view=self).build)

        def open_relatorio_professor(page):  # Função para abrir o Relatório de Professores
            load_content(RelatorioProfessoresView(main_view=self).build)

        def open_horario_manual(page):
            load_content(HorarioManualView(main_view=self).build)

        def open_exportar_horario(page):
            load_content(ExportarHorarioView(main_view=self).build)

        def open_cadastrar_sala(page):
            load_content(CadastrarSalaView(main_view=self).build)

        def open_consultar_editar_sala(page):
            load_content(ConsultarEditarSalaView(main_view=self).build)

        def open_relatorio_sala(page):
            load_content(RelatorioSalaView(main_view=self).build)

        def limpar_area_conteudo():
            self.content_area.controls.clear()

            page.update()

        self.limpar_area_conteudo = limpar_area_conteudo

        # Submenus para Professores
        submenu_professores = ft.Column(
            controls=[
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Cadastrar Professor"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_cadastrar_professor(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Consultar/Editar Professor"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_consultar_editar_professor(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Excluir Professor"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_excluir_professor(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Relatório Professores"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_relatorio_professor(page)  # Ação para abrir o Relatório de Professores
                ),
            ],
            visible=False,
            spacing=5,
        )

        # Submenus para Disciplinas
        submenu_disciplinas = ft.Column(
            controls=[
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Cadastrar Disciplina"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_cadastrar_disciplina(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Consultar/Editar Disciplina"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_consultar_editar_disciplina(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Excluir Disciplina"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_excluir_disciplina(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Relatório"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_relatorio_disciplina(page)
                ),
            ],
            visible=False,
            spacing=5,
        )

        # Submenus para Horários
        submenu_horarios = ft.Column(
            controls=[
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Horário Manual"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_horario_manual(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Exportar Horário"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_exportar_horario(page)
                ),
            ],
            visible=False,
            spacing=5,
        )

        # Submenus para Salas
        submenu_salas = ft.Column(
            controls=[
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Cadastrar Sala"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_cadastrar_sala(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Consultar/Editar Sala"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_consultar_editar_sala(page)
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Text("Relatório"),
                        alignment=ft.alignment.center_left,
                        padding=ft.padding.symmetric(vertical=10, horizontal=20),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREY_900,
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    on_click=lambda e: open_relatorio_sala(page)
                ),
            ],
            visible=False,
            spacing=5,
        )

        self.content_area = ft.Column(expand=True, auto_scroll=True)

        menu = ft.Container(
            content=ft.Column(
                controls=[
                    # Menu Professores
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.PERSON, color=ft.colors.WHITE),
                                        ft.Text(value="Professores", color=ft.colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=10,
                                ),
                                padding=ft.padding.symmetric(vertical=15, horizontal=10),
                                alignment=ft.alignment.center_left,
                            ),
                            on_click=lambda e: toggle_submenu(e, submenu_professores),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.GREY_900,
                                shape=ft.RoundedRectangleBorder(radius=0)
                            )
                        ),
                        width=250  # Largura fixa para a barra lateral
                    ),
                    ft.Container(submenu_professores, padding=ft.padding.only(left=20)),

                    # Menu Disciplinas
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.BOOK, color=ft.colors.WHITE),
                                        ft.Text(value="Disciplinas", color=ft.colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=10,
                                ),
                                padding=ft.padding.symmetric(vertical=15, horizontal=10),
                                alignment=ft.alignment.center_left,
                            ),
                            on_click=lambda e: toggle_submenu(e, submenu_disciplinas),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.GREY_900,
                                shape=ft.RoundedRectangleBorder(radius=0)
                            )
                        ),
                        width=250  # Largura fixa para a barra lateral
                    ),
                    ft.Container(submenu_disciplinas, padding=ft.padding.only(left=20)),

                    # Menu Horários
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.DATE_RANGE, color=ft.colors.WHITE),
                                        ft.Text(value="Horários", color=ft.colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=10),
                                padding=ft.padding.symmetric(vertical=15, horizontal=10),
                                alignment=ft.alignment.center_left,
                            ),
                            on_click=lambda e: toggle_submenu(e, submenu_horarios),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.GREY_900,
                                shape=ft.RoundedRectangleBorder(radius=0)
                            )
                        ),
                        width=250  # Largura fixa para a barra lateral
                    ),
                    ft.Container(submenu_horarios, padding=ft.padding.only(left=20)),

                    # Menu Salas
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.HOME, color=ft.colors.WHITE),
                                        ft.Text(value="Salas", color=ft.colors.WHITE),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=10),
                                padding=ft.padding.symmetric(vertical=15, horizontal=10),
                                alignment=ft.alignment.center_left,
                            ),
                            on_click=lambda e: toggle_submenu(e, submenu_salas),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.GREY_900,
                                shape=ft.RoundedRectangleBorder(radius=0)
                            )
                        ),
                        width=250  # Largura fixa para a barra lateral
                    ),
                    ft.Container(submenu_salas, padding=ft.padding.only(left=20)),
                ],
                spacing=10,
                expand=True,  # Expande a altura da barra lateral
            ),
            width=260,  # Largura fixa para a barra lateral
            height=5000,
            bgcolor=ft.colors.GREY_900,
            padding=ft.padding.all(0),
            alignment=ft.alignment.center_left,
            expand=False
        )

        page.add(
            ft.Row(
                controls=[
                    menu,
                    self.content_area
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                expand=True
            )
        )

        page.update()

if __name__ == "__main__":
    MainView().run()
