import flet as ft

class GoalsPage(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        def create_goal_card(title, target, current):
            progress = current / target
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Target: ${target:,.2f}"),
                    ft.Text(f"Current: ${current:,.2f}"),
                    ft.ProgressBar(value=progress, width=300),
                    ft.Text(f"{progress:.0%} Complete", size=16),
                ]),
                width=350,
                padding=20,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            )

        goals = [
            create_goal_card("Emergency Fund", 10000, 5000),
            create_goal_card("Down Payment for House", 50000, 15000),
            create_goal_card("Retirement Savings", 500000, 100000),
            create_goal_card("Vacation Fund", 5000, 2500),
        ]

        goals_grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=350,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=20,
        )

        for goal in goals:
            goals_grid.controls.append(goal)

        main_content = ft.Column([
            ft.Text("Financial Goals", size=32, weight=ft.FontWeight.BOLD),
            goals_grid,
        ], scroll=ft.ScrollMode.AUTO)

        return main_content