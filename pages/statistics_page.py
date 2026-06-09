import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import services


def show_statistics_page(parent):
    page = StatisticsPage(parent)
    page.pack(fill="both", expand=True)

class StatisticsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F5F5F5")

        self.create_header()
        self.create_summary_cards()
        self.create_chart_section()
        self.create_low_stock_table()


    # = FORMAT RUPIAH
    def format_rupiah(self, value):
        return f"Rp {int(value):,}".replace(",", ".")


    # = HEADER
    def create_header(self):
        header = tk.Frame(self, bg="#F5F5F5")
        header.pack(fill="x", padx=30, pady=(20, 10))

        title = tk.Label(
            header,
            text="Store Statistics",
            font=("Arial", 22, "bold"),
            bg="#F5F5F5",
            fg="#222222"
        )
        title.pack(side="left")

        refresh_button = tk.Button(
            header,
            text="Refresh",
            font=("Arial", 10),
            bg="#2563EB",
            fg="white",
            padx=12,
            pady=5,
            command=self.refresh_statistics
        )
        refresh_button.pack(side="right")


    # = CREATE SUMMARY CARD
    def create_summary_card(self, parent, title, value, row, column):
        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        )
        title_label.pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111111"
        )
        value_label.pack(anchor="w", pady=(5, 0))


    # = SUMMARY CARDS
    def create_summary_cards(self):
        summary = services.get_statistics_summary()

        card_container = tk.Frame(self, bg="#F5F5F5")
        card_container.pack(fill="x", padx=30, pady=(0, 10))

        for column in range(3):
            card_container.grid_columnconfigure(column, weight=1)

        self.create_summary_card(
            card_container,
            "Total Produk",
            summary["total_products"],
            0,
            0
        )

        self.create_summary_card(
            card_container,
            "Total Stok",
            summary["total_stock"],
            0,
            1
        )

        self.create_summary_card(
            card_container,
            "Nilai Inventori",
            self.format_rupiah(summary["total_inventory_value"]),
            0,
            2
        )

        # self.create_summary_card(
        #     card_container,
        #     "Total Transaksi",
        #     summary["total_transactions"],
        #     1,
        #     0
        # )

        # self.create_summary_card(
        #     card_container,
        #     "Total Pendapatan",
        #     self.format_rupiah(summary["total_sales_revenue"]),
        #     1,
        #     1
        # )

        self.create_summary_card(
            card_container,
            "Promosi Aktif",
            summary["total_active_promotions"],
            1,
            2
        )


    # = CHART SECTION
    def create_chart_section(self):
        chart_container = tk.Frame(self, bg="#F5F5F5")
        chart_container.pack(fill="both", expand=True, padx=30, pady=10)

        left_chart = tk.Frame(chart_container, bg="white", bd=1, relief="solid")
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_chart = tk.Frame(chart_container, bg="white", bd=1, relief="solid")
        right_chart.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self.create_best_selling_chart(left_chart)
        self.create_revenue_chart(right_chart)


    # = BEST SELLING CHART
    def create_best_selling_chart(self, parent):
        product_names, quantities = services.get_quantity_chart_data()

        figure = Figure(figsize=(5, 3), dpi=100)
        chart = figure.add_subplot(111)

        if len(product_names) == 0:
            chart.text(
                0.5,
                0.5,
                "Belum ada data penjualan",
                ha="center",
                va="center"
            )
        else:
            chart.bar(product_names, quantities)
            chart.set_title("Produk Terlaris")
            chart.set_ylabel("Jumlah Terjual")
            chart.tick_params(axis="x", rotation=20)

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    # = REVENUE CHART
    def create_revenue_chart(self, parent):
        product_names, revenues = services.get_revenue_chart_data()

        figure = Figure(figsize=(5, 3), dpi=100)
        chart = figure.add_subplot(111)

        if len(product_names) == 0:
            chart.text(
                0.5,
                0.5,
                "Belum ada data pendapatan",
                ha="center",
                va="center"
            )
        else:
            chart.bar(product_names, revenues)
            chart.set_title("Pendapatan Per Produk")
            chart.set_ylabel("Pendapatan")
            chart.tick_params(axis="x", rotation=20)

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    # = LOW STOCK TABLE
    def create_low_stock_table(self):
        table_frame = tk.Frame(self, bg="#F5F5F5")
        table_frame.pack(fill="x", padx=30, pady=(5, 20))

        title = tk.Label(
            table_frame,
            text="Produk Stok Rendah",
            font=("Arial", 14, "bold"),
            bg="#F5F5F5",
            fg="#222222"
        )
        title.pack(anchor="w", pady=(0, 8))

        columns = (
            "id",
            "name",
            "category",
            "stock",
            "status"
        )

        self.low_stock_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        self.low_stock_table.heading("id", text="ID")
        self.low_stock_table.heading("name", text="Nama Produk")
        self.low_stock_table.heading("category", text="Kategori")
        self.low_stock_table.heading("stock", text="Stok")
        self.low_stock_table.heading("status", text="Status")

        self.low_stock_table.column("id", width=80, anchor="center")
        self.low_stock_table.column("name", width=250)
        self.low_stock_table.column("category", width=150, anchor="center")
        self.low_stock_table.column("stock", width=100, anchor="center")
        self.low_stock_table.column("status", width=120, anchor="center")

        self.low_stock_table.pack(fill="x")

        self.load_low_stock_products()


    # = LOAD LOW STOCK PRODUCTS
    def load_low_stock_products(self):
        for item in self.low_stock_table.get_children():
            self.low_stock_table.delete(item)

        low_stock_products = services.get_low_stock_products(limit_stock=5)

        for product in low_stock_products:
            self.low_stock_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["name"],
                    product["category"],
                    product["stock"],
                    product["status"]
                )
            )


    # = REFRESH STATISTICS
    def refresh_statistics(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_summary_cards()
        self.create_chart_section()
        self.create_low_stock_table()