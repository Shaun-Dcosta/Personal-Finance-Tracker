import flet as ft
from datetime import datetime

class IncomePage(ft.UserControl):
    def __init__(self):
        super().__init__()
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
        self.accounts_dropdown = ft.Dropdown(
            label="Account",
            options=[
                ft.dropdown.Option("Checking Account"),
                ft.dropdown.Option("Savings Account"),
                ft.dropdown.Option("Investment Account"),
                ft.dropdown.Option("Cash"),
            ],
            width=200,
        )
        self.submit_button = ft.ElevatedButton("Add Income", on_click=self.add_income)

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
                            ft.DataColumn(ft.Text("Source")),
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Frequency")),
                        ],
                        rows=[
                            ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2]))]) 
                            for row in data
                        ],
                    )
                ]),
                width=300,
                margin=ft.margin.only(top=10),
            )

        income_data = [
            ("Salary", "$4,000", "Monthly"),
            ("Freelance", "$800", "Monthly"),
            ("Investments", "$600", "Monthly"),
            ("Gifts", "$200", "Annually"),
        ]

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
            self.accounts_dropdown,
            self.submit_button,
        ], spacing=10, width=400)

        main_content = ft.ResponsiveRow([
            ft.Column([
                ft.Text("Income Overview", size=28, weight=ft.FontWeight.BOLD),
                chart_and_table,
            ], col={"sm": 12, "md": 6}),
            ft.Column([input_form], col={"sm": 12, "md": 6}),
        ], spacing=20)

        return main_content

    def add_income(self, e):
        print("Amount:", self.amount_input.value)
        print("Type:", self.type_dropdown.value)
        print("Date:", self.date_picker.value.value)
        print("Account:", self.accounts_dropdown.value)

        self.amount_input.value = ""
        self.type_dropdown.value = None
        self.date_picker.value.value = None
        self.accounts_dropdown.value = None
        self.update()

def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    
    income_page = IncomePage()
    page.add(income_page)
    page.overlay.append(income_page.date_picker)
    page.update()

ft.app(target=main)