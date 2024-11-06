import flet as ft
from datetime import datetime

class DebtsPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.debt_data = []

    def build(self):
        def create_pie_chart(data, colors, icons):
            normal_radius = 100
            hover_radius = 110
            normal_title_style = ft.TextStyle(
                size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
            )
            hover_title_style = ft.TextStyle(
                size=16,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
            )
            normal_badge_size = 40
            hover_badge_size = 50

            def badge(icon, size):
                return ft.Container(
                    ft.Icon(icon),
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

        debt_chart = ft.Container(
            content=create_pie_chart(
                [40, 30, 20, 10],
                [ft.colors.RED, ft.colors.ORANGE, ft.colors.YELLOW, ft.colors.GREEN],
                [ft.icons.HOME, ft.icons.CREDIT_CARD, ft.icons.SCHOOL, ft.icons.DIRECTIONS_CAR]
            ),
            width=400,
            height=400,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            alignment=ft.alignment.center,
        )

        def create_data_table(title, data):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Type")),
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Due Date")),
                            ft.DataColumn(ft.Text("Status")),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(row[0])),
                                    ft.DataCell(ft.Text(f"${row[1]:.2f}")),
                                    ft.DataCell(ft.Text(row[2].strftime("%Y-%m-%d"))),
                                    ft.DataCell(ft.Text(row[3]))
                                ]
                            ) 
                            for row in data
                        ],
                    )
                ]),
                width=600,
                margin=ft.margin.only(top=20),
            )

        self.debt_table = create_data_table("Debt Details", self.debt_data)

        def add_debt(e):
            if not amount.value or not due_date.value:
                return
            
            new_debt = (
                debt_type.value,
                float(amount.value),
                datetime.strptime(due_date.value, "%Y-%m-%d"),
                status.value
            )
            self.debt_data.append(new_debt)
            self.debt_table.content.controls[1].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(new_debt[0])),
                        ft.DataCell(ft.Text(f"${new_debt[1]:.2f}")),
                        ft.DataCell(ft.Text(new_debt[2].strftime("%Y-%m-%d"))),
                        ft.DataCell(ft.Text(new_debt[3]))
                    ]
                )
            )
            amount.value = ""
            due_date.value = ""
            self.debt_table.update()

        amount = ft.TextField(label="Amount", width=150)
        debt_type = ft.Dropdown(
            label="Type",
            width=150,
            options=[
                ft.dropdown.Option("Loan"),
                ft.dropdown.Option("Credit Card"),
                ft.dropdown.Option("Mortgage"),
            ],
        )
        due_date = ft.TextField(label="Due Date (YYYY-MM-DD)", width=200)
        status = ft.Dropdown(
            label="Status",
            width=150,
            options=[
                ft.dropdown.Option("Completed"),
                ft.dropdown.Option("Due"),
            ],
        )

        input_row = ft.Row(
            [amount, debt_type, due_date, status, ft.ElevatedButton("Add Debt", on_click=add_debt)],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        main_content = ft.Column([
            ft.Text("Debt Overview", size=32, weight=ft.FontWeight.BOLD),
            ft.Row([debt_chart, self.debt_table], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            input_row,
        ], scroll=ft.ScrollMode.AUTO)

        return main_content
    
def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    
    debts_page = DebtsPage()
    page.add(debts_page)

ft.app(target=main)