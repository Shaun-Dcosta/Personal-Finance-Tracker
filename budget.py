import flet as ft

class BudgetPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.sidebar = None
        self.amount_input = ft.TextField(label="Amount", prefix_text="$", width=150)
        self.category_dropdown = ft.Dropdown(
            label="Category",
            options=[
                ft.dropdown.Option("Groceries"),
                ft.dropdown.Option("Water"),
                ft.dropdown.Option("Electricity"),
                ft.dropdown.Option("Clothes"),
                ft.dropdown.Option("Other"),
            ],
            width=150,
        )
        self.submit_button = ft.ElevatedButton("Add Expense", on_click=self.add_expense)

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

        budget_chart = ft.Container(
            content=create_pie_chart(
                [30, 25, 20, 15, 10],
                [ft.colors.BLUE, ft.colors.GREEN, ft.colors.ORANGE, ft.colors.PURPLE, ft.colors.PINK],
                [ft.icons.HOME, ft.icons.FASTFOOD, ft.icons.DIRECTIONS_CAR, ft.icons.SHOPPING_BAG, ft.icons.MOVIE]
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
                            ft.DataColumn(ft.Text("Category")),
                            ft.DataColumn(ft.Text("Allocated")),
                            ft.DataColumn(ft.Text("Spent")),
                            ft.DataColumn(ft.Text("Remaining")),
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

        budget_data = [
            ("Housing", "$1,000", "$950", "$50"),
            ("Food", "$500", "$450", "$50"),
            ("Transportation", "$400", "$380", "$20"),
            ("Shopping", "$300", "$250", "$50"),
            ("Entertainment", "$200", "$180", "$20"),
        ]

        budget_table = create_data_table("Budget Breakdown", budget_data)

        input_form = ft.Column([
            ft.Text("Add New Expense", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.amount_input,
                self.category_dropdown,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.submit_button,
        ], spacing=10)

        main_content = ft.ResponsiveRow([
            ft.Column([
                ft.Text("Budget Overview", size=28, weight=ft.FontWeight.BOLD),
                budget_chart,
                budget_table,
            ], col={"sm": 12, "md": 6}),
            ft.Column([input_form], col={"sm": 12, "md": 6}),
        ], spacing=10)

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

    def add_expense(self, e):
        print("Amount:", self.amount_input.value)
        print("Category:", self.category_dropdown.value)
        self.amount_input.value = ""
        self.category_dropdown.value = None
        self.update()

def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    
    budget_page = BudgetPage()
    page.add(budget_page)

ft.app(target=main)