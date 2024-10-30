import flet as ft
import mysql.connector as mysql

con=mysql.connect(host='localhost',user='root',password='mysql@123',database='pft',port='3306')
cursor=con.cursor()

class TransactionsPage(ft.UserControl):
    def __init__(self):
        super().__init__()

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
                            ft.DataColumn(ft.Text("Recepient")),
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

        pull_transactions="select amount,category,timestamp,acc_number,recepient from transactions"
        cursor.execute(pull_transactions)
        transactions_data=cursor.fetchall()

        transactions_table = create_data_table("Transaction List", transactions_data)

        main_content = ft.Column([
            ft.Text("Transactions", size=32, weight=ft.FontWeight.BOLD),
            transactions_table,
        ], scroll=ft.ScrollMode.AUTO)

        return main_content
    
def main(page: ft.Page):
    page.title = "Personal Finance Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    transactions_page=TransactionsPage()
    page.add(transactions_page)

ft.app(target=main)