import tkinter as tk
from tkinter import ttk
from utils.formatter import format_rupiah

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

import services


def show_statistics_page(parent):
    page = StatisticsPage(parent)
    page.pack(fill="both", expand=True)


class StatisticsPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#F3F4F6")

        self.create_scroll_area()
        self.load_page()


    # CREATE SCROLL AREA
    def create_scroll_area(self):
        self.canvas = tk.Canvas(
            self,
            bg="#F3F4F6",
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.content_frame = tk.Frame(
            self.canvas,
            bg="#F3F4F6"
        )

        self.content_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )


    # LOAD PAGE
    def load_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_summary_cards()
        self.create_chart_section()
        self.create_table_section()


    # HEADER
    def create_header(self):
        header = tk.Frame(
            self.content_frame,
            bg="#F3F4F6"
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title = tk.Label(
            header,
            text="Store Statistics",
            font=("Arial", 24, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header,
            text="Rangkuman terkait produk, promosi, dan transaksi",
            font=("Arial", 11),
            bg="#F3F4F6",
            fg="#4B5563"
        )
        subtitle.pack(
            side="left",
            padx=20,
            pady=(8, 0)
        )

        refresh_button = tk.Button(
            header,
            text="Refresh",
            font=("Arial", 10),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            padx=15,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=self.load_page
        )
        refresh_button.pack(side="right")


    # CREATE CARD
    def create_card(self, parent, title, value, subtitle, row, column):
        card = tk.Frame(
            parent,
            bg="white",
            padx=18,
            pady=14
        )
        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#6B7280"
        )
        title_label.pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        )
        value_label.pack(
            anchor="w",
            pady=(5, 2)
        )

        subtitle_label = tk.Label(
            card,
            text=subtitle,
            font=("Arial", 9),
            bg="white",
            fg="#6B7280"
        )
        subtitle_label.pack(anchor="w")


    # SUMMARY CARDS
    def create_summary_cards(self):
        summary = services.get_statistics_summary()

        promotion_summary = summary["promotion_summary"]
        highest_inventory_product = summary["highest_inventory_value_product"]

        container = tk.Frame(
            self.content_frame,
            bg="#F3F4F6"
        )
        container.pack(
            fill="x",
            padx=30
        )

        for column in range(3):
            container.grid_columnconfigure(column, weight=1)

        self.create_card(
            container,
            "Rata-rata Harga Produk",
            format_rupiah(summary["average_product_price"]),
            "Ringkasan dari Manage Products",
            0,
            0
        )

        self.create_card(
            container,
            "Produk Nilai Tertinggi",
            highest_inventory_product["name"],
            format_rupiah(highest_inventory_product["inventory_value"]),
            0,
            1
        )

        self.create_card(
            container,
            "Promosi Aktif",
            summary["total_active_promotions"],
            "Ringkasan dari Manage Promotions",
            0,
            2
        )

        self.create_card(
            container,
            "Total Diskon Diberikan",
            format_rupiah(promotion_summary["total_discount_given"]),
            "Dari transaksi yang memakai promo",
            1,
            0
        )

        self.create_card(
            container,
            "Total Pendapatan",
            format_rupiah(summary["total_sales_revenue"]),
            "Ringkasan dari Manage Transactions",
            1,
            1
        )

        self.create_card(
            container,
            "Barang Terjual",
            summary["total_items_sold"],
            "Total quantity transaksi keluar",
            1,
            2
        )


    # CHART SECTION
    def create_chart_section(self):
        chart_container = tk.Frame(
            self.content_frame,
            bg="#F3F4F6"
        )
        chart_container.pack(
            fill="x",
            padx=30,
            pady=(15, 10)
        )

        chart_container.grid_columnconfigure(0, weight=1)
        chart_container.grid_columnconfigure(1, weight=1)

        left_chart = tk.Frame(
            chart_container,
            bg="white",
            padx=10,
            pady=10
        )
        left_chart.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(8, 8)
        )

        right_chart = tk.Frame(
            chart_container,
            bg="white",
            padx=10,
            pady=10
        )
        right_chart.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 8)
        )

        self.create_best_selling_chart(left_chart)
        self.create_revenue_chart(right_chart)


    # BEST SELLING CHART
    def create_best_selling_chart(self, parent):
        product_names, quantities = services.get_quantity_chart_data(limit=5)

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
            chart.set_xticks([])
            chart.set_yticks([])
        else:
            chart.bar(product_names, quantities)
            chart.set_title(
                "Top Produk Terlaris",
                fontsize=12,
                fontweight="bold"
            )
            chart.set_ylabel("Jumlah Terjual")
            chart.tick_params(axis="x", rotation=20)

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # REVENUE CHART
    def create_revenue_chart(self, parent):
        product_names, revenues = services.get_revenue_chart_data(limit=5)

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
            chart.set_xticks([])
            chart.set_yticks([])
        else:
            chart.bar(product_names, revenues)
            chart.set_title(
                "Top Pendapatan Produk",
                fontsize=12,
                fontweight="bold"
            )
            chart.set_ylabel("Pendapatan")
            
            chart.yaxis.set_major_formatter(
                FuncFormatter(lambda value, position: format_rupiah(value))
            )
            chart.tick_params(axis="x", rotation=20)
            
            

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # TABLE SECTION
    def create_table_section(self):
        table_container = tk.Frame(
            self.content_frame,
            bg="#F3F4F6"
        )
        table_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 30)
        )

        self.create_promotion_sales_table(table_container)
        self.create_recent_transaction_table(table_container)


    # CREATE SECTION TITLE
    def create_section_title(self, parent, text):
        title = tk.Label(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        )
        title.pack(
            anchor="w",
            pady=(15, 8)
        )


    # PROMOTION SALES TABLE
    def create_promotion_sales_table(self, parent):
        self.create_section_title(parent, "Performa Promosi")

        columns = (
            "promotion_id",
            "product_name",
            "discount_percent",
            "total_quantity",
            "total_revenue",
            "total_discount",
            "status"
        )

        table = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=5
        )

        table.heading("promotion_id", text="ID Promo")
        table.heading("product_name", text="Nama Produk")
        table.heading("discount_percent", text="Diskon")
        table.heading("total_quantity", text="Terjual")
        table.heading("total_revenue", text="Pendapatan Promo")
        table.heading("total_discount", text="Total Diskon")
        table.heading("status", text="Status")

        table.column("promotion_id", width=80, anchor="center")
        table.column("product_name", width=260)
        table.column("discount_percent", width=80, anchor="center")
        table.column("total_quantity", width=90, anchor="center")
        table.column("total_revenue", width=160, anchor="e")
        table.column("total_discount", width=160, anchor="e")
        table.column("status", width=100, anchor="center")

        table.pack(fill="x")

        promotion_sales = services.get_promotion_sales_by_product()

        for promotion in promotion_sales:
            table.insert(
                "",
                "end",
                values=(
                    promotion["promotion_id"],
                    promotion["product_name"],
                    f'{promotion["discount_percent"]}%',
                    promotion["total_quantity"],
                    format_rupiah(promotion["total_revenue"]),
                    format_rupiah(promotion["total_discount"]),
                    promotion["status"]
                )
            )


    # RECENT TRANSACTION TABLE
    def create_recent_transaction_table(self, parent):
        self.create_section_title(parent, "Transaksi Terbaru")

        columns = (
            "id",
            "product_name",
            "type",
            "quantity",
            "total_price",
            "date",
            "status"
        )

        table = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=5
        )

        table.heading("id", text="ID")
        table.heading("product_name", text="Nama Produk")
        table.heading("type", text="Tipe")
        table.heading("quantity", text="Jumlah")
        table.heading("total_price", text="Total")
        table.heading("date", text="Tanggal")
        table.heading("status", text="Status")

        table.column("id", width=80, anchor="center")
        table.column("product_name", width=260)
        table.column("type", width=100, anchor="center")
        table.column("quantity", width=100, anchor="center")
        table.column("total_price", width=160, anchor="e")
        table.column("date", width=180, anchor="center")
        table.column("status", width=120, anchor="center")

        table.pack(fill="x")

        recent_transactions = services.get_recent_transactions(limit=5)

        for transaction in recent_transactions:
            table.insert(
                "",
                "end",
                values=(
                    transaction["id"],
                    transaction["product_name"],
                    transaction["type"],
                    transaction["quantity"],
                    format_rupiah(transaction["total_price"]),
                    transaction["date"],
                    transaction["status"]
                )
            )