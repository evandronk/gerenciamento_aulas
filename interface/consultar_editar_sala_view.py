import flet as ft

class ConsultarEditarSalaView:
    def __init__(self, main_view):
        self.main_view = main_view

    def build(self, page: ft.Page):
        return ft.Container(
            content=ft.Text("Consultar/Editar Sala", size=30),
            padding=20
        )
