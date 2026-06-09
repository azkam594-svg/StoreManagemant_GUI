import tkinter as tk
from tkinter import ttk, messagebox
from services.transactions_service import (
    calculate_balance,
    export_transactions_csv,
    get_transactions,
    get_transaction_summary,
    record_transaction,
)

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

    def create_header(self):
        title = tk.Label(
            self,
            text="Manage Transactions",
            font=("Arial", 24, "bold"),
            bg="#E9E9E9",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=30, pady=(30, 15))

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

        self.balance_label = tk.Label(
            summary_frame,
            text="Total Pendapatan: Rp 0",
            font=("Arial", 11, "bold"),
            bg="#E9E9E9",
            fg="#0f766e"
        )
        self.balance_label.pack(side="left")

    def create_table(self):

        columns = (
            "id",
            "sku",
            "type",
            "quantity",
            "amount",
            "date"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.table.heading(col, text=col.upper())

        self.table.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

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
            text="SKU:",
            bg="#E9E9E9",
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky="w")

        self.sku_entry = tk.Entry(form_frame, width=18)
        self.sku_entry.grid(row=0, column=3, padx=10, pady=5)

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

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        self.load_transactions()
        self.refresh_summary()

    def load_transactions(self):
        from services.transactions_service import get_transaction_amount

        for t in get_transactions():
            amount = get_transaction_amount(t)
            self.table.insert(
                "",
                "end",
                values=(
                    t.get("id"),
                    t.get("sku"),
                    t.get("type"),
                    t.get("quantity"),
                    f"Rp {amount:,}",
                    t.get("date"),
                ),
            )

    def refresh_summary(self):
        summary = get_transaction_summary()
        self.masuk_label.config(text=f"Transaksi Masuk: {summary['masuk']}")
        self.keluar_label.config(text=f"Transaksi Keluar: {summary['keluar']}")
        self.total_label.config(text=f"Total Transaksi: {summary['total']}")
        self.balance_label.config(
            text=f"Total Pendapatan: Rp {summary['total_sales']:,}"
        )

    def add_transaction(self):
        sku = self.sku_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()
        transaction_type = self.type_var.get()

        try:
            quantity = int(quantity_text)
            record_transaction(sku, quantity, transaction_type)
            messagebox.showinfo(
                "Transaksi Disimpan",
                f"Transaksi {transaction_type} untuk SKU {sku} berhasil disimpan."
            )
            self.sku_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")
            self.refresh_table()
        except ValueError as error:
            messagebox.showwarning("Kesalahan Transaksi", str(error))
        except Exception as error:
            messagebox.showerror("Kesalahan", str(error))

    def show_balance(self):
        total = calculate_balance()
        messagebox.showinfo(
            "Saldo Store",
            f"Total Pendapatan: Rp {total:,}"
        )

    def export_csv(self):
        file = export_transactions_csv()
        messagebox.showinfo(
            "Export CSV",
            f"Data berhasil diexport ke {file}"
        )