import flet as ft
import os

def main(page: ft.Page):
    page.title = "Homepage"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f4f8"
    page.fonts = {
        "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "Roboto-Bold": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
    }

    def logout(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Logout Successful"),
            content=ft.Text("You have been logged out successfully."),
            on_dismiss=lambda _: (os.system('python login_signup.py'), page.window_destroy())
        )
        page.dialog.open = True
        page.update()

    # AppBar
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.HOME),
        leading_width=40,
        title=ft.Text("Homepage"),
        center_title=False,
        bgcolor=ft.colors.BLUE_600,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Profile"),
                    ft.PopupMenuItem(text="Settings"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Logout", on_click=logout),
                ]
            ),
        ],
    )

    # Welcome message
    welcome_message = ft.Text(
        "Welcome to Your Dashboard",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_600,
    )

    # Stats
    stats_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Total Users", size=20, color=ft.colors.BLUE_GREY_400),
                        ft.Text("1,234", size=36, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                width=200,
                height=150,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.BLUE_GREY_100,
                    offset=ft.Offset(0, 0),
                ),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Active Sessions", size=20, color=ft.colors.BLUE_GREY_400),
                        ft.Text("56", size=36, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                width=200,
                height=150,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.BLUE_GREY_100,
                    offset=ft.Offset(0, 0),
                ),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("New Messages", size=20, color=ft.colors.BLUE_GREY_400),
                        ft.Text("7", size=36, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                width=200,
                height=150,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.BLUE_GREY_100,
                    offset=ft.Offset(0, 0),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Recent  activity
    recent_activity = ft.Container(
        content=ft.Column(
            [
                ft.Text("Recent Activity", size=24, weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("User")),
                        ft.DataColumn(ft.Text("Action")),
                        ft.DataColumn(ft.Text("Time")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("John Doe")),
                                ft.DataCell(ft.Text("Logged in")),
                                ft.DataCell(ft.Text("2 minutes ago")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Jane Smith")),
                                ft.DataCell(ft.Text("Updated profile")),
                                ft.DataCell(ft.Text("15 minutes ago")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Bob Johnson")),
                                ft.DataCell(ft.Text("Sent a message")),
                                ft.DataCell(ft.Text("1 hour ago")),
                            ],
                        ),
                    ],
                ),
            ],
            spacing=20,
        ),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLUE_GREY_100,
            offset=ft.Offset(0, 0),
        ),
    )

    # Main content
    page.add(
        ft.Column(
            [
                welcome_message,
                ft.Container(height=20),
                stats_row,
                ft.Container(height=20),
                recent_activity,
            ],
            spacing=10,
        )
    )

ft.app(target=main)