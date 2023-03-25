from nicegui import ui


class Base:
    def __init__(self):
        ui.add_head_html("<link rel='stylesheet' href='/static/style.css' />")
        ui.add_head_html("<script src='/static/script.js'> </script>")

        self.base = ui.column().classes("main")
