import flet as ft
from homepage import HomePage
from transactions import TransactionsPage
from income import IncomePage
from budget import BudgetPage
from debts import DebtsPage
from goals import GoalsPage

def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    def toggle_sidebar(e):
        sidebar.visible = not sidebar.visible
        page.update()

    def logout(e):
        print("Logout clicked")

    sidebar = ft.Container(
        content=ft.Column([
            ft.TextButton("Homepage", on_click=lambda _: page.go("/")),
            ft.TextButton("Transactions", on_click=lambda _: page.go("/transactions")),
            ft.TextButton("Income", on_click=lambda _: page.go("/income")),
            ft.TextButton("Budget", on_click=lambda _: page.go("/budget")),
            ft.TextButton("Debts", on_click=lambda _: page.go("/debts")),
            ft.TextButton("Goals", on_click=lambda _: page.go("/goals")),
        ]),
        width=200,
        bgcolor=ft.colors.SURFACE_VARIANT,
        visible=False
    )

    top_bar = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar),
            ft.Text("Financial Management App", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.IconButton(ft.icons.ACCOUNT_CIRCLE, on_click=lambda _: print("Profile clicked")),
                ft.IconButton(ft.icons.LOGOUT, on_click=logout),
            ]),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=10,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    pages = {
        "/": HomePage(),
        "/transactions": TransactionsPage(),
        "/income": IncomePage(),
        "/budget": BudgetPage(),
        "/debts": DebtsPage(),
        "/goals": GoalsPage(),
    }

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route.route,
                [
                    ft.Row([
                        sidebar,
                        ft.VerticalDivider(width=1),
                        ft.Column([top_bar, pages[route.route]], expand=True),
                    ], expand=True)
                ],
            )
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)