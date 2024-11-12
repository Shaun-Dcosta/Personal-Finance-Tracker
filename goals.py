import flet as ft
import mysql.connector as mysql
from datetime import datetime

# Connect to MySQL database
con = mysql.connect(host='localhost', user='root', password='mysql@123', database='pft', port='3306')
cursor = con.cursor()

class GoalsPage(ft.UserControl):
    def __init__(self, username:str):
        super().__init__()
        self.username=username
        query = "SELECT user_id FROM user WHERE username = %s"
        cursor.execute(query, (self.username,))
        self.user_id = cursor.fetchone()[0]
        self.goals = self.fetch_goals()

    def fetch_goals(self):
        # Fetch initial goals data from MySQL
        query = "SELECT type, target, amount_saved, status, doc, target_date FROM goals WHERE user_id = %s"
        cursor.execute(query, (self.user_id,))
        goals_data = cursor.fetchall()
        return [
            {
                "type": row[0],
                "target": row[1],
                "amount_saved": row[2],
                "status": row[3],
                "creation_date": row[4].strftime("%Y-%m-%d"),
                "target_date": row[5].strftime("%Y-%m-%d")
            } for row in goals_data
        ]

    def build(self):
        # Function to create a goal card UI component
        def create_goal_card(goal, index):
            progress = goal["amount_saved"] / goal["target"] if goal["target"] > 0 else 0

            def update_goal(e):
                updated_goal = {
                    "type": goal_type_update.value,
                    "target": float(target_update.value),
                    "amount_saved": float(amount_saved_update.value),
                    "status": status_update.value,
                    "creation_date": creation_date_update.value,
                    "target_date": target_date_update.value,
                }

                # Update MySQL database
                query = """
                    UPDATE goals
                    SET type = %s, target = %s, amount_saved = %s, status = %s, doc = %s, target_date = %s
                    WHERE user_id = %s AND type = %s
                """
                cursor.execute(query, (
                    updated_goal["type"],
                    updated_goal["target"],
                    updated_goal["amount_saved"],
                    updated_goal["status"],
                    updated_goal["creation_date"],
                    updated_goal["target_date"],
                    self.user_id,
                    goal["type"]
                ))
                con.commit()

                # Update goal in memory and refresh the UI
                self.goals[index] = updated_goal
                update_goals_list()

            # Input fields to edit a goal
            goal_type_update = ft.TextField(value=goal["type"], width=100, height=35)
            target_update = ft.TextField(value=str(goal["target"]), width=80, height=35)
            amount_saved_update = ft.TextField(value=str(goal["amount_saved"]), width=80, height=35)
            status_update = ft.Dropdown(
                value=goal["status"],
                width=100,
                height=35,
                options=[
                    ft.dropdown.Option("In Progress"),
                    ft.dropdown.Option("Reached"),
                ],
            )
            creation_date_update = ft.TextField(value=goal["creation_date"], width=100, height=35)
            target_date_update = ft.TextField(value=goal["target_date"], width=100, height=35)

            # Create goal card layout
            return ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(goal["type"], size=16, weight=ft.FontWeight.BOLD),
                        ft.ProgressBar(value=progress, width=150, height=5),
                        ft.Text(f"{progress:.0%} Complete", size=12),
                    ], spacing=2),
                    ft.Column([
                        ft.Text(f"Target: ${goal['target']:,.2f}", size=12),
                        ft.Text(f"Current: ${goal['amount_saved']:,.2f}", size=12),
                        ft.Text(f"Status: {goal['status']}", size=12),
                    ], spacing=2),
                    ft.Column([
                        goal_type_update,
                        ft.Row([target_update, amount_saved_update], spacing=5),
                        ft.Row([status_update, creation_date_update, target_date_update], spacing=5),
                        ft.ElevatedButton("Update", on_click=update_goal, height=35),
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                width=800,
                padding=10,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=5,
            )

        self.goals_list = ft.ListView(spacing=10, padding=20, auto_scroll=True)

        def update_goals_list():
            self.goals_list.controls.clear()
            for index, goal in enumerate(self.goals):
                self.goals_list.controls.append(create_goal_card(goal, index))
            self.goals_list.update()

        def add_goal(e):
            if not all([goal_type.value, target.value, amount_saved.value, status.value, creation_date.value, target_date.value]):
                return

            new_goal = {
                "type": goal_type.value,
                "target": float(target.value),
                "amount_saved": float(amount_saved.value),
                "status": status.value,
                "creation_date": creation_date.value,
                "target_date": target_date.value,
            }

            # Insert new goal into MySQL database
            query = """
                INSERT INTO goals (user_id, type, target, amount_saved, status, doc, target_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.user_id,
                new_goal["type"],
                new_goal["target"],
                new_goal["amount_saved"],
                new_goal["status"],
                new_goal["creation_date"],
                new_goal["target_date"],
            ))
            con.commit()

            # Add goal to list and refresh UI
            self.goals.append(new_goal)
            update_goals_list()

            # Clear input fields
            goal_type.value = ""
            target.value = ""
            amount_saved.value = ""
            status.value = None
            creation_date.value = ""
            target_date.value = ""
            self.update()

        # Input fields for adding a new goal
        goal_type = ft.TextField(label="Goal Type", width=150, height=35)
        target = ft.TextField(label="Target Amount", width=120, height=35)
        amount_saved = ft.TextField(label="Amount Saved", width=120, height=35)
        status = ft.Dropdown(
            label="Status",
            width=120,
            height=35,
            options=[
                ft.dropdown.Option("In Progress"),
                ft.dropdown.Option("Reached"),
            ],
        )
        creation_date = ft.TextField(label="Creation Date", width=150, height=35)
        target_date = ft.TextField(label="Target Date", width=150, height=35)

        input_row = ft.Row(
            [
                goal_type,
                target,
                amount_saved,
                status,
                creation_date,
                target_date,
                ft.ElevatedButton("Add Goal", on_click=add_goal, height=35)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        main_content = ft.Column([
            ft.Text("Financial Goals", size=24, weight=ft.FontWeight.BOLD),
            input_row,
            self.goals_list,
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

        return main_content
    
def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    
    goals_page = GoalsPage('test')  # Replace with actual user_id
    page.add(goals_page)

ft.app(target=main)
