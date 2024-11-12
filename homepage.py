import flet as ft
import mysql.connector as mysql
from transactions import TransactionsPage

con = mysql.connect(
    host='localhost',
    user='root',
    password='mysql@123',
    database='pft',
    port='3306'
)
cursor = con.cursor()

class HomePage(ft.UserControl):    
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        print(self.username)
        self.sidebar = None
        self.normal_radius = 130
        self.hover_radius = 10
        self.normal_title_style = ft.TextStyle(
            size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        self.hover_title_style = ft.TextStyle(
            size=16,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )
        self.normal_badge_size = 40
        self.hover_badge_size = 50

    def toggle_sidebar(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.update()

    def logout(self, e):
        print("Logout clicked")

    def badge(self, icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
        )

    def create_pie_chart(self, data, colors, icons):
        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = self.hover_radius
                    section.title_style = self.hover_title_style
                    section.badge.width = self.hover_badge_size
                    section.badge.height = self.hover_badge_size
                    section.badge.border_radius = self.hover_badge_size / 2
                else:
                    section.radius = self.normal_radius
                    section.title_style = self.normal_title_style
                    section.badge.width = self.normal_badge_size
                    section.badge.height = self.normal_badge_size
                    section.badge.border_radius = self.normal_badge_size / 2
            chart.update()

        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    value,
                    title=f"{value}%",
                    title_style=self.normal_title_style,
                    color=color,
                    radius=self.normal_radius,
                    badge=self.badge(icon, self.normal_badge_size),
                    badge_position=0.98,
                )
                for value, color, icon in zip(data, colors, icons)
            ],
            sections_space=0,
            center_space_radius=0,
            on_chart_event=on_chart_event,
            expand=True,
        )
        return chart

    def create_data_table(self, title, data):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Date")),
                        ft.DataColumn(ft.Text("Category")),
                        ft.DataColumn(ft.Text("Amount")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2]))]) 
                        for row in data
                    ],
                )
            ]),
            width=450,
            margin=ft.margin.only(top=20),
        )

    def build(self):
        def open_transactions_page(e):
            transactions_page = TransactionsPage(self.username)
            self.page.clean()
            self.page.add(transactions_page)
            self.page.update()

        self.sidebar = ft.Container(
            content=ft.Column([
                ft.TextButton("Homepage", on_click=lambda _: print("Homepage clicked")),
                ft.TextButton("Transactions", on_click=open_transactions_page),  # Modified this line
                ft.TextButton("Income", on_click=lambda _: print("Income clicked")),
                ft.TextButton("Budget", on_click=lambda _: print("Budget clicked")),
                ft.TextButton("Debts", on_click=lambda _: print("Debts clicked")),
                ft.TextButton("Goals", on_click=lambda _: print("Goals clicked")),
            ]),
            width=200,
            height=770,
            bgcolor=ft.colors.SURFACE_VARIANT,
            visible=False
        )

        top_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.icons.MENU, on_click=self.toggle_sidebar),
                ft.Text("Financial Management App", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Text(f"Welcome, {self.username}", size=16),
                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, on_click=lambda _: print("Profile clicked")),
                    ft.IconButton(ft.icons.LOGOUT, on_click=self.logout),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        pie_chart_container = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=self.create_pie_chart(
                        [40, 30, 15, 15],
                        [ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PURPLE, ft.colors.GREEN],
                        [ft.icons.HOME, ft.icons.SHOPPING_CART, ft.icons.DIRECTIONS_CAR, ft.icons.MOVIE]
                    ),
                    width=300,
                    height=300,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=self.create_pie_chart(
                        [35, 25, 20, 20],
                        [ft.colors.RED, ft.colors.ORANGE, ft.colors.CYAN, ft.colors.PINK],
                        [ft.icons.ATTACH_MONEY, ft.icons.SAVINGS, ft.icons.CREDIT_CARD, ft.icons.ACCOUNT_BALANCE]
                    ),
                    width=300,
                    height=300,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            margin=ft.margin.only(top=20),
        )

        transactions_data = [
            ("2023-05-01", "Groceries", "$50.00"),
            ("2023-05-02", "Gas", "$30.00"),
            ("2023-05-03", "Dinner", "$45.00"),
            ("2023-05-04", "Movie", "$20.00"),
            ("2023-05-05", "Utilities", "$100.00"),
        ]

        debt_payments_data = [
            ("2023-05-15", "Credit Card", "$200.00"),
            ("2023-05-20", "Student Loan", "$150.00"),
            ("2023-05-25", "Car Loan", "$300.00"),
            ("2023-05-30", "Mortgage", "$1000.00"),
            ("2023-06-01", "Personal Loan", "$100.00"),
        ]

        tables_container = ft.Container(
            content=ft.Row([
                self.create_data_table("Recent Transactions", transactions_data),
                self.create_data_table("Upcoming Debt Payments", debt_payments_data),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            margin=ft.margin.only(top=20, left=20, right=20),
        )

        main_content = ft.Column([
            pie_chart_container,
            tables_container,
        ], scroll=ft.ScrollMode.AUTO)

        return ft.Row([
            self.sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([top_bar, main_content], expand=True),
        ], expand=True)
    
# def init_homepage(page: ft.Page, username: str):
#     page.title = "Personal Finance Tracker"
#     page.theme_mode = ft.ThemeMode.DARK
#     page.padding = 0
    
#     home_page = HomePage(username)
#     page.add(home_page)
#     page.update()