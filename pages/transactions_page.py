import tkinter as tk
import services

from tkinter import ttk, messagebox
from utils.formatter import format_rupiah




def show_transactions_page(parent):
    page = TransactionPage(parent)
    page.pack(fill="both", expand=True)


class TransactionPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#E9E9E9")

        self.create_header()
        self.create_summary_frame()
        self.create_toolbar()
        self.create_table()
        self.create_add_transaction_form()
        self.refresh_table()


    # HEADER
    def create_header(self):
        title = tk.Label(
            self,
            text="Manage Transactions",
            font=("Arial", 24, "bold"),
            bg="#E9E9E9",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=30, pady=(30, 15))


    # TOOLBAR
    def create_toolbar(self):
        toolbar = tk.Frame(self, bg="#E9E9E9")
        toolbar.pack(fill="x", padx=30)

        tk.Button(
            toolbar,
            text="Cek Saldo",
            bg="#16a34a",
            fg="white",
            command=self.show_balance
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Export CSV",
            bg="#2563eb",
            fg="white",
            command=self.export_csv
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Segarkan",
            bg="#6b7280",
            fg="white",
            command=self.refresh_table
        ).pack(side="left", padx=5)
        

    # SUMMARY
    def create_summary_frame(self):
        summary_frame = tk.Frame(self, bg="#E9E9E9")
        summary_frame.pack(fill="x", padx=30, pady=(10, 0))

        self.masuk_label = tk.Label(
            summary_frame,
            text="Transaksi Masuk: 0",
            font=("Arial", 11),
            bg="#E9E9E9",
            fg="#111827"
        )
        self.masuk_label.pack(side="left", padx=(0, 20))

        self.keluar_label = tk.Label(
            summary_frame,
            text="Transaksi Keluar: 0",
            font=("Arial", 11),
            bg="#E9E9E9",
            fg="#111827"
        )
        self.keluar_label.pack(side="left", padx=(0, 20))

        self.total_label = tk.Label(
            summary_frame,
            text="Total Transaksi: 0",
            font=("Arial", 11),
            bg="#E9E9E9",
            fg="#111827"
        )
        self.total_label.pack(side="left", padx=(0, 20))

        
        # BALANCE CARD
        balance_card = tk.Frame(
            summary_frame,
            bg="#F0FDF4",
            bd=1,
            relief="solid",
            padx=0,
            pady=0
        )
        balance_card.pack(side="right", padx=5, pady=5)

        # Aksen hijau di kiri card
        accent = tk.Frame(
            balance_card,
            bg="#16A34A",
            width=5
        )
        accent.pack(side="left", fill="y")

        balance_content = tk.Frame(
            balance_card,
            bg="#F0FDF4",
            padx=18,
            pady=10
        )
        balance_content.pack(side="left", fill="both")

        balance_title = tk.Label(
            balance_content,
            text="Total Pendapatan",
            font=("Arial", 10),
            bg="#F0FDF4",
            fg="#166534"
        )
        balance_title.pack(anchor="e")

        self.balance_label = tk.Label(
            balance_content,
            text="Rp 0",
            font=("Arial", 18, "bold"),
            bg="#F0FDF4",
            fg="#15803D"
        )
        self.balance_label.pack(anchor="e", pady=(3, 0))
        
        
        # EXPENSE CARD
        expense_card = tk.Frame(
            summary_frame,
            bg="#FEF2F2",
            bd=1,
            relief="solid",
            padx=0,
            pady=0
        )
        expense_card.pack(side="right", padx=5, pady=5)

        expense_accent = tk.Frame(
            expense_card,
            bg="#DC2626",
            width=5
        )
        expense_accent.pack(side="left", fill="y")

        expense_content = tk.Frame(
            expense_card,
            bg="#FEF2F2",
            padx=18,
            pady=10
        )
        expense_content.pack(side="left", fill="both")

        expense_title = tk.Label(
            expense_content,
            text="Total Pengeluaran",
            font=("Arial", 10),
            bg="#FEF2F2",
            fg="#991B1B"
        )
        expense_title.pack(anchor="e")

        self.expense_label = tk.Label(
            expense_content,
            text="Rp 0",
            font=("Arial", 18, "bold"),
            bg="#FEF2F2",
            fg="#DC2626"
        )
        self.expense_label.pack(anchor="e", pady=(3, 0))

    # TABLE
    def create_table(self):
        table_frame = tk.Frame(self, bg="#E9E9E9")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        columns = (
            "id",
            "product_id",
            "product_name",
            "type",
            "quantity",
            "price",
            "discount_percent",
            "final_price",
            "total_price",
            "date",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("product_id", text="ID Produk")
        self.table.heading("product_name", text="Nama Produk")
        self.table.heading("type", text="Tipe")
        self.table.heading("quantity", text="Jumlah")
        self.table.heading("price", text="Harga Asli")
        self.table.heading("discount_percent", text="Diskon")
        self.table.heading("final_price", text="Harga Akhir")
        self.table.heading("total_price", text="Total")
        self.table.heading("date", text="Tanggal")
        self.table.heading("status", text="Status")

        self.table.column("id", width=60, anchor="center")
        self.table.column("product_id", width=90, anchor="center")
        self.table.column("product_name", width=180)
        self.table.column("type", width=90, anchor="center")
        self.table.column("quantity", width=80, anchor="center")
        self.table.column("price", width=120, anchor="e")
        self.table.column("discount_percent", width=80, anchor="center")
        self.table.column("final_price", width=120, anchor="e")
        self.table.column("total_price", width=130, anchor="e")
        self.table.column("date", width=160, anchor="center")
        self.table.column("status", width=100, anchor="center")

        y_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        x_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        self.table.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)


    # ADD TRANSACTION FORM
    def create_add_transaction_form(self):
        form_frame = tk.LabelFrame(
            self,
            text="Tambah Transaksi Penjualan / Pembelian",
            bg="#E9E9E9",
            font=("Arial", 12, "bold"),
            fg="#111827",
            padx=15,
            pady=15
        )
        form_frame.pack(fill="x", padx=30, pady=(0, 20))

        tk.Label(
            form_frame,
            text="Tipe:",
            bg="#E9E9E9",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w")

        self.type_var = tk.StringVar(value="Keluar")

        self.type_selector = ttk.Combobox(
            form_frame,
            textvariable=self.type_var,
            values=("Keluar", "Masuk"),
            state="readonly",
            width=14
        )
        self.type_selector.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            form_frame,
            text="ID Produk:",
            bg="#E9E9E9",
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky="w")

        self.product_id_entry = tk.Entry(form_frame, width=18)
        self.product_id_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(
            form_frame,
            text="Jumlah:",
            bg="#E9E9E9",
            font=("Arial", 10)
        ).grid(row=0, column=4, sticky="w")

        self.quantity_entry = tk.Entry(form_frame, width=10)
        self.quantity_entry.grid(row=0, column=5, padx=10, pady=5)

        tk.Button(
            form_frame,
            text="Simpan Transaksi",
            bg="#2563eb",
            fg="white",
            command=self.add_transaction
        ).grid(row=0, column=6, padx=10, pady=5)


    # REFRESH TABLE
    def refresh_table(self):
        self.table.delete(*self.table.get_children())

        self.load_transactions()
        self.refresh_summary()


    # LOAD TRANSACTIONS
    def load_transactions(self):
        transaction_list = services.get_transactions()

        for transaction in transaction_list:
            self.table.insert(
                "",
                "end",
                values=(
                    transaction.get("id"),
                    transaction.get("product_id"),
                    transaction.get("product_name"),
                    transaction.get("type"),
                    transaction.get("quantity"),
                    format_rupiah(transaction.get("price", 0)),
                    f"{transaction.get('discount_percent', 0)}%",
                    format_rupiah(transaction.get("final_price", 0)),
                    format_rupiah(transaction.get("total_price", 0)),
                    transaction.get("date"),
                    transaction.get("status"),
                )
            )


    # REFRESH SUMMARY
    def refresh_summary(self):
        summary = services.get_transaction_summary()

        self.masuk_label.config(
            text=f"Transaksi Masuk: {summary['masuk']}"
        )

        self.keluar_label.config(
            text=f"Transaksi Keluar: {summary['keluar']}"
        )

        self.total_label.config(
            text=f"Total Transaksi: {summary['total']}"
        )

        self.balance_label.config(
            text=format_rupiah(summary["total_sales"])
        )

        self.expense_label.config(
            text=format_rupiah(summary["total_expense"])
        )



# BUTTON CALLBACK
    # ADD TRANSACTION
    def add_transaction(self):
        product_id = self.product_id_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        transaction_type = self.type_var.get()

        try:
            services.record_transaction(
                product_id=product_id,
                quantity=quantity,
                transaction_type=transaction_type
            )

            messagebox.showinfo(
                "Transaksi Disimpan",
                f"Transaksi {transaction_type} untuk produk ID {product_id} berhasil disimpan."
            )

            self.product_id_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")

            self.refresh_table()

        except ValueError as error:
            messagebox.showwarning("Kesalahan Transaksi", str(error))

        except Exception as error:
            messagebox.showerror("Kesalahan", str(error))

    # SHOW BALANCE
    def show_balance(self):
        summary = services.get_transaction_summary()

        messagebox.showinfo(
            "Saldo Store",
            f"Total Pendapatan: {format_rupiah(summary['total_sales'])}\n"
            f"Total Pengeluaran: {format_rupiah(summary['total_expense'])}\n"
            f"Saldo Bersih: {format_rupiah(summary['net_balance'])}"
        )

    # EXPORT CSV
    def export_csv(self):
        file = services.export_transactions_csv()

        messagebox.showinfo(
            "Export CSV",
            f"Data berhasil diexport ke {file}"
        )