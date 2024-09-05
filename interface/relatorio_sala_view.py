import flet as ft

class RelatorioSalaView:
    def __init__(self, main_view):
        self.main_view = main_view

    def build(self, page: ft.Page):
        return ft.Container(
            content=ft.Text("Relatório de Salas", size=30),
            padding=20
        )
