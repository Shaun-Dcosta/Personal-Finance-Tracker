import flet as ft
from datetime import datetime
import mysql.connector as mysql

con = mysql.connect(host='localhost', user='root', password='mysql@123', database='pft', port='3306')
cursor = con.cursor()

class IncomePage(ft.UserControl):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        y = "select user_id from user where username=%s"
        cursor.execute(y, (self.username,))
        self.user_id = cursor.fetchone()[0]
        self.sidebar = None
        self.amount_input = ft.TextField(label="Amount", prefix_text="$", width=200)
        self.type_dropdown = ft.Dropdown(
            label="Income Type",
            options=[
                ft.dropdown.Option("Earned"),
                ft.dropdown.Option("Passive"),
                ft.dropdown.Option("Capital Gains"),
                ft.dropdown.Option("Rental"),
                ft.dropdown.Option("Pension"),
                ft.dropdown.Option("Commissions"),
                ft.dropdown.Option("Other"),
            ],
            width=200,
        )
        self.date_picker = ft.DatePicker(
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2030, 12, 31),
        )
        self.date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_TODAY,
            on_click=lambda _: self.date_picker.pick_date(),
        )
        self.account_input = ft.TextField(label="Account Number", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        self.submit_button = ft.ElevatedButton("Add Income", on_click=self.add_income)

    def toggle_sidebar(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.update()

    def logout(self, e):
        print("Logout clicked")

    def build(self):
        def create_pie_chart(data, colors, icons):
            normal_radius = 80
            hover_radius = 90
            normal_title_style = ft.TextStyle(
                size=10, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
            )
            hover_title_style = ft.TextStyle(
                size=14,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
            )
            normal_badge_size = 30
            hover_badge_size = 40

            def badge(icon, size):
                return ft.Container(
                    ft.Icon(icon, size=14),
                    width=size,
                    height=size,
                    border=ft.border.all(1, ft.colors.BROWN),
                    border_radius=size / 2,
                    bgcolor=ft.colors.WHITE,
                )

            def on_chart_event(e: ft.PieChartEvent):
                for idx, section in enumerate(chart.sections):
                    if idx == e.section_index:
                        section.radius = hover_radius
                        section.title_style = hover_title_style
                        section.badge.width = hover_badge_size
                        section.badge.height = hover_badge_size
                        section.badge.border_radius = hover_badge_size / 2
                    else:
                        section.radius = normal_radius
                        section.title_style = normal_title_style
                        section.badge.width = normal_badge_size
                        section.badge.height = normal_badge_size
                        section.badge.border_radius = normal_badge_size / 2
                chart.update()

            chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(
                        value,
                        title=f"{value}%",
                        title_style=normal_title_style,
                        color=color,
                        radius=normal_radius,
                        badge=badge(icon, normal_badge_size),
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

        income_chart = ft.Container(
            content=create_pie_chart(
                [60, 20, 15, 5],
                [ft.colors.BLUE, ft.colors.GREEN, ft.colors.ORANGE, ft.colors.PURPLE],
                [ft.icons.WORK, ft.icons.ATTACH_MONEY, ft.icons.SAVINGS, ft.icons.CARD_GIFTCARD]
            ),
            width=300,
            height=300,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            alignment=ft.alignment.center,
        )

        def create_data_table(title, data):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Type")),
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Timestamp")),
                            ft.DataColumn(ft.Text("Account Number")),
                        ],
                        rows=[
                            ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2])), ft.DataCell(ft.Text(row[3]))]) 
                            for row in data
                        ],
                    )
                ]),
                width=300,
                margin=ft.margin.only(top=10),
            )

        pull_income = "SELECT type,amount,timestamp,acc_number from income where user_id=%s"
        cursor.execute(pull_income, (self.user_id,))
        income_data = cursor.fetchall()

        income_table = create_data_table("Income Sources", income_data)

        chart_and_table = ft.Column([
            income_chart,
            income_table,
        ], spacing=10)

        input_form = ft.Column([
            ft.Text("Add New Income", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.amount_input, self.type_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                self.date_button,
                ft.Text("Selected date: ", weight=ft.FontWeight.BOLD),
                ft.Text(ref=self.date_picker.value),
            ]),
            self.account_input,
            self.submit_button,
        ], spacing=10, width=400)

        main_content = ft.ResponsiveRow([
            ft.Column([
                ft.Text("Income Overview", size=28, weight=ft.FontWeight.BOLD),
                chart_and_table,
            ], col={"sm": 12, "md": 6}),
            ft.Column([input_form], col={"sm": 12, "md": 6}),
        ], spacing=20)

        # Sidebar
        self.sidebar = ft.Container(
            content=ft.Column([
                ft.TextButton("Homepage", on_click=lambda _: print("Homepage clicked")),
                ft.TextButton("Transactions", on_click=lambda _: print("Transactions clicked")),
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

        # Top bar
        top_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.icons.MENU, on_click=self.toggle_sidebar),
                ft.Text("Financial Management App", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, on_click=lambda _: print("Profile clicked")),
                    ft.IconButton(ft.icons.LOGOUT, on_click=self.logout),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        return ft.Row([
            self.sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([top_bar, main_content], expand=True),
        ], expand=True)

    def add_income(self, e):
        # Get the input values
        amount = self.amount_input.value
        income_type = self.type_dropdown.value
        timestamp = self.date_picker.value
        account_number = self.account_input.value

        if not amount or not income_type or not timestamp or not account_number:
            return

        income_insert = "INSERT INTO income(type, amount, timestamp, acc_number, user_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(income_insert, (income_type, amount, timestamp, account_number, self.user_id))
        con.commit()

        # Clear the input fields
        self.amount_input.value = ""
        self.type_dropdown.value = None
        self.date_picker.value.value = None
        self.account_input.value = ""
        
        # Re-fetch updated income data
        pull_income = "SELECT type, amount, timestamp, acc_number FROM income WHERE user_id=%s"
        cursor.execute(pull_income, (self.user_id,))
        updated_income_data = cursor.fetchall()

        # Rebuild the income table with the new data
        self.income_table.content = ft.Column([
            ft.Text("Income Sources", size=16, weight=ft.FontWeight.BOLD),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Type")),
                    ft.DataColumn(ft.Text("Amount")),
                    ft.DataColumn(ft.Text("Timestamp")),
                    ft.DataColumn(ft.Text("Account Number")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row[0])),
                        ft.DataCell(ft.Text(row[1])),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3]))
                    ]) for row in updated_income_data
                ],
            )
        ])
    

        self.update()

def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    
    income_page = IncomePage("test")
    page.add(income_page)
    page.overlay.append(income_page.date_picker)
    page.update()

ft.app(target=main)
