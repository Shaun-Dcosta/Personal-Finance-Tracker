import flet as ft

def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    def toggle_sidebar(e):
        sidebar.visible = not sidebar.visible
        page.update()

    def logout(e):
        print("Logout clicked")

    # Pie chart configuration
    normal_radius = 130
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

    def create_pie_chart(data, colors, icons):
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

    sidebar = ft.Container(
        content=ft.Column([
            ft.TextButton("Homepage", on_click=lambda _: print("Homepage clicked")),
            ft.TextButton("Transactions", on_click=lambda _: print("Transactions clicked")),
            ft.TextButton("Income", on_click=lambda _: print("Income clicked")),
            ft.TextButton("Budget", on_click=lambda _: print("Budget clicked")),
            ft.TextButton("Debts", on_click=lambda _: print("Debts clicked")),
            ft.TextButton("Goals", on_click=lambda _: print("Goals clicked")),
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

    pie_chart_container = ft.Container(
        content=ft.Row([
            ft.Container(
                content=create_pie_chart(
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
                content=create_pie_chart(
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

    def create_data_table(title, data):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Date")),
                        ft.DataColumn(ft.Text("Description")),
                        ft.DataColumn(ft.Text("Amount")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2]))]) 
                        for row in data
                    ],
                )
            ]),
            width=400,
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
            create_data_table("Recent Transactions", transactions_data),
            create_data_table("Upcoming Debt Payments", debt_payments_data),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        margin=ft.margin.only(top=20, left=20, right=20),
    )

    main_content = ft.Column([
        pie_chart_container,
        tables_container,
    ], scroll=ft.ScrollMode.AUTO)

    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([top_bar, main_content], expand=True),
        ], expand=True)
    )

ft.app(target=main)