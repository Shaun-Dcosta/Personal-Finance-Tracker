import flet as ft

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
                            ft.DataColumn(ft.Text("Date")),
                            ft.DataColumn(ft.Text("Description")),
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Category")),
                        ],
                        rows=[
                            ft.DataRow(cells=[ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(row[2])), ft.DataCell(ft.Text(row[3]))]) 
                            for row in data
                        ],
                    )
                ]),
                width=800,
                margin=ft.margin.only(top=20),
            )

        transactions_data = [
            ("2023-05-01", "Groceries", "$50.00", "Food"),
            ("2023-05-02", "Gas", "$30.00", "Transportation"),
            ("2023-05-03", "Dinner", "$45.00", "Food"),
            ("2023-05-04", "Movie", "$20.00", "Entertainment"),
            ("2023-05-05", "Utilities", "$100.00", "Bills"),
            ("2023-05-06", "Clothing", "$75.00", "Shopping"),
            ("2023-05-07", "Coffee", "$5.00", "Food"),
            ("2023-05-08", "Gym Membership", "$50.00", "Health"),
            ("2023-05-09", "Books", "$30.00", "Education"),
            ("2023-05-10", "Phone Bill", "$60.00", "Bills"),
        ]

        transactions_table = create_data_table("Recent Transactions", transactions_data)

        main_content = ft.Column([
            ft.Text("Transactions", size=32, weight=ft.FontWeight.BOLD),
            transactions_table,
        ], scroll=ft.ScrollMode.AUTO)

        return main_content