print(r"""
 _   _ ______        ____        __  _                    _           
| | | |  _ \ \      / /\ \      / / | |    ___   __ _  __| | ___ _ __ 
| |_| | | | \ \ /\ / /  \ \ /\ / /  | |   / _ \ / _` |/ _` |/ _ \ '__|
|  _  | |_| |\ V  V /    \ V  V /   | |__| (_) | (_| | (_| |  __/ |   
|_| |_|____/  \_/\_/      \_/\_/    |_____\___/ \__,_|\__,_|\___|_|   
""") #remove this if you don't want it

import flet as ft
import subprocess
import sys
import os

slow_mode_enabled = False

def main(page: ft.Page):
    page.title = "HDWW"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    py_file_path = r"PATH TO n.py HERE" #put the path to the n.py here

    def run_n_py(model_name):
        if os.path.exists(py_file_path):
            try:
                result = subprocess.run([sys.executable, py_file_path, model_name, str(slow_mode_enabled)], capture_output=True, text=True)
                print(f"Debug Opened n.py with model {model_name} (Slow Mode: {slow_mode_enabled})")
                print(result.stdout)
                if result.stderr:
                    print("{Error} " + result.stderr)
            except Exception as ex:
                print("{Error} Could not open file: " + str(ex))
        else:
            print("{Error} The file 'n.py' does not exist at the specified path.")

    def n_click(e):
        run_n_py("yolov10n.pt")

    def x_click(e):
        run_n_py("yolov10x.pt")

    def toggle_slow_mode(e):
        global slow_mode_enabled
        slow_mode_enabled = e.control.value
        print(f"Slow Mode: {'Enabled' if slow_mode_enabled else 'Disabled'}")

    column = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=n_click),
                    ft.IconButton(ft.icons.ADD, on_click=x_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            ft.Row(
                [
                    ft.Checkbox(label="Slow Mode", on_change=toggle_slow_mode),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(column)

ft.app(main)
