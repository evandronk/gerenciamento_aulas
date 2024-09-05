import flet as ft

class ExportarHorarioView:
    def __init__(self, main_view):
        self.main_view = main_view

    def build(self, page: ft.Page):
        return ft.Container(
            content=ft.Text("Exportar Horário", size=30),
            padding=20
        )
