import flet as ft
import mysql.connector as mysql
from datetime import datetime

con = mysql.connect(host='localhost', user='root', password='mysql@123', database='pft', port='3306')
cursor = con.cursor()

class AccountsPage(ft.UserControl):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        y = "select user_id from user where username=%s"
        cursor.execute(y, (self.username,))
        self.user_id = cursor.fetchone()[0]
        self.accounts = []
        self.sidebar = None
        self.new_account_number = ft.TextField(label="Account Number", width=200)
        self.new_account_type = ft.Dropdown(
            label="Account Type",
            options=[
                ft.dropdown.Option("current"),
                ft.dropdown.Option("savings"),
                ft.dropdown.Option("fixed deposit"),
                ft.dropdown.Option("salary"),
                ft.dropdown.Option("nri"),
                ft.dropdown.Option("recurring deposit"),
            ],
            width=200,
        )
        self.new_balance = ft.TextField(label="Balance", width=200, prefix_text="$")
        self.new_date_of_creation = ft.TextField(label="Date of Creation (YYYY-MM-DD)", width=200)
        self.new_minimum_balance = ft.TextField(label="Minimum Balance", width=200, prefix_text="$")
        self.submit_button = ft.ElevatedButton("Add Account", on_click=self.add_account)
        self.accounts_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Account Number")),
                ft.DataColumn(ft.Text("Type")),
                ft.DataColumn(ft.Text("Balance")),
                ft.DataColumn(ft.Text("Date of Creation")),
                ft.DataColumn(ft.Text("Minimum Balance")),
            ],
            rows=[]
        )
        # Load accounts immediately upon initialization
        self.load_accounts()

    def toggle_sidebar(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.update()

    def logout(self, e):
        print("Logout clicked")

    def build(self):
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

        main_content = ft.Column([
            ft.Text("Accounts", size=28, weight=ft.FontWeight.BOLD),
            self.accounts_table,
            ft.Divider(),
            ft.Text("Add New Account", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.new_account_number, self.new_account_type], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([self.new_balance, self.new_date_of_creation], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.new_minimum_balance,
            self.submit_button,
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

        return ft.Row([
            self.sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([top_bar, main_content], expand=True),
        ], expand=True)

    def add_account(self, e):
        try:
            account_number = self.new_account_number.value
            account_type = self.new_account_type.value
            balance = float(self.new_balance.value)
            date_of_creation = datetime.strptime(self.new_date_of_creation.value, "%Y-%m-%d").date()
            minimum_balance = float(self.new_minimum_balance.value)

            new_account = {
                "account_number": account_number,
                "type": account_type,
                "balance": balance,
                "date_of_creation": date_of_creation,
                "minimum_balance": minimum_balance
            }

            account_add = "insert into accounts(acc_number, type, balance, doc, min_balance, user_id) values(%s, %s, %s, %s, %s, %s)"
            cursor.execute(account_add, (account_number, account_type, balance, date_of_creation, minimum_balance, self.user_id))
            con.commit()

            self.accounts.append(new_account)
            self.update_table()
            self.clear_inputs()
        except ValueError:
            print("Invalid input. Please check your entries.")

    def update_table(self):
        self.accounts_table.rows.clear()
        for account in self.accounts:
            self.accounts_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(account["account_number"])),
                        ft.DataCell(ft.Text(account["type"])),
                        ft.DataCell(ft.Text(f"${account['balance']:.2f}")),
                        ft.DataCell(ft.Text(account["date_of_creation"].strftime("%Y-%m-%d"))),
                        ft.DataCell(ft.Text(f"${account['minimum_balance']:.2f}")),
                    ]
                )
            )
        self.update()

    def clear_inputs(self):
        self.new_account_number.value = ""
        self.new_account_type.value = None
        self.new_balance.value = ""
        self.new_date_of_creation.value = ""
        self.new_minimum_balance.value = ""
        self.update()

    def load_accounts(self):
        try:
            query = "SELECT acc_number, type, balance, doc, min_balance FROM accounts WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            for row in rows:
                account = {
                    "account_number": row[0],
                    "type": row[1],
                    "balance": row[2],
                    "date_of_creation": row[3],
                    "minimum_balance": row[4]
                }
                self.accounts.append(account)
            self.update_table()
        except Exception as e:
            print(f"Error loading accounts: {e}")
        
def main(page: ft.Page):
    page.title = "Accounts Page"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    accounts_page = AccountsPage("Shaun")
    page.add(accounts_page)
    page.update()

ft.app(target=main)
