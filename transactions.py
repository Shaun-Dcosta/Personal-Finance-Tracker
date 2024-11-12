import flet as ft
import mysql.connector as mysql
from datetime import datetime
import mysql.connector as mysql

con=mysql.connect(host='localhost',user='root',password='mysql@123',database='pft',port='3306')
cursor=con.cursor()

class TransactionsPage(ft.UserControl):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        y="select user_id from user where username=%s"
        cursor.execute(y,(self.username,))
        self.user_id=cursor.fetchone()[0]
        print(self.username, "tran")
        self.transactions_table = None
        self.sidebar = None

    def toggle_sidebar(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.update()

    def logout(self, e):
        print("Logout clicked")

    def navigate_to_home(self, e):
        from homepage import HomePage 
        home_page = HomePage(self.username)
        self.page.clean()
        self.page.add(home_page)
        self.page.update()

    def build(self):
        def create_data_table(title, data):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Category")),
                            ft.DataColumn(ft.Text("Timestamp")),
                            ft.DataColumn(ft.Text("From Account")),
                            ft.DataColumn(ft.Text("Recipient")),
                        ],
                        rows=[
                            ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2])), ft.DataCell(ft.Text(row[3])), ft.DataCell(ft.Text(row[4]))]) 
                            for row in data
                        ],
                    )
                ]),
                width=800,
                margin=ft.margin.only(top=20),
            )

        def update_transactions_table():
            pull_transactions = "SELECT amount, category, timestamp, acc_number, recepient FROM transactions where user_id=%s"
            cursor.execute(pull_transactions,(self.user_id,))
            transactions_data = cursor.fetchall()
            self.transactions_table.content.controls[1].rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2])), ft.DataCell(ft.Text(row[3])), ft.DataCell(ft.Text(row[4]))]) 
                for row in transactions_data
            ]
            self.update()

        def submit_transaction(e):
            amount = float(amount_input.value)
            category = category_dropdown.value
            timestamp = datetime.strptime(date_picker.value, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
            recipient = recipient_input.value
            acc_number = "12345"  # Placeholder account number

            insert_query = "INSERT INTO transactions (amount, category, timestamp, acc_number, recepient,user_id) VALUES (%s, %s, %s, %s, %s,%s)"
            cursor.execute(insert_query, (amount, category, timestamp, acc_number, recipient))
            con.commit()

            update_transactions_table()
            amount_input.value = ""
            category_dropdown.value = None
            date_picker.value = None
            recipient_input.value = ""
            self.update()

        # Sidebar
        self.sidebar = ft.Container(
            content=ft.Column([
                ft.TextButton("Homepage", on_click=self.navigate_to_home),
                ft.TextButton("Transactions", on_click=lambda _: print("Transactions clicked")),
                ft.TextButton("Income", on_click=lambda _: print("Income clicked")),
                ft.TextButton("Budget", on_click=lambda _: print("Budget clicked")),
                ft.TextButton("Debts", on_click=lambda _: print("Debts clicked")),
                ft.TextButton("Goals", on_click=lambda _: print("Goals clicked")),
            ]),
            width=200,
            height=770,
            bgcolor=ft.colors.SURFACE_VARIANT,
            visible=True  # Changed to True for consistency
        )

        # Top bar
        top_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.icons.MENU, on_click=self.toggle_sidebar),
                ft.Text("Financial Management App", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Text(f"Welcome, {self.username}", size=16),  # Added username display
                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, on_click=lambda _: print("Profile clicked")),
                    ft.IconButton(ft.icons.LOGOUT, on_click=self.logout),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        amount_input = ft.TextField(label="Amount", width=200)
        category_dropdown = ft.Dropdown(
            label="Category",
            width=200,
            options=[
                ft.dropdown.Option("Groceries"),
                ft.dropdown.Option("Electricity"),
                ft.dropdown.Option("Water"),
                ft.dropdown.Option("Clothes"),
                ft.dropdown.Option("Other"),
            ],
        )
        date_picker = ft.TextField(label="Date", width=200)
        recipient_input = ft.TextField(label="Recipient", width=200)
        submit_button = ft.ElevatedButton("Add Transaction", on_click=submit_transaction)

        form_row = ft.Row([amount_input, category_dropdown, date_picker, recipient_input, submit_button], alignment=ft.MainAxisAlignment.CENTER)

        pull_transactions = "SELECT amount, category, timestamp, acc_number, recepient FROM transactions where user_id=%s"
        cursor.execute(pull_transactions,(self.user_id,))
        transactions_data = cursor.fetchall()

        self.transactions_table = create_data_table("Transaction List", transactions_data)

        main_content = ft.Column([
            ft.Text("Transactions", size=32, weight=ft.FontWeight.BOLD),
            form_row,
            self.transactions_table,
        ], scroll=ft.ScrollMode.AUTO)

        return ft.Row([
            self.sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([top_bar, main_content], expand=True),
        ], expand=True)


# def main(page: ft.Page):
#     page.title = "Personal Finance Tracker"
#     page.theme_mode = ft.ThemeMode.DARK
#     page.padding = 0
    
#     transactions_page = TransactionsPage('Shaun')
#     page.add(transactions_page)

# ft.app(target=main)