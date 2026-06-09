import tkinter as tk
from tkinter import ttk

import services
from utils import formatter


def show_dashboard_page(parent):
    page = DashboardPage(parent)
    page.pack(fill="both", expand=True)
    
    
class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#E0E0E0")
        
        self.create_header()
        self.create_summary_cards()
        self.create_low_stock_section()
    
    # HEADER
    def create_header(self):
        title = tk.Label(
            self,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="#E0E0E0",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=30, pady=(30, 15))
        
        subtitle = tk.Label(
            self,
            text="Ringkasan Informasi Produk dan Inventori toko",
            font=("Arial", 14),
            bg="#E0E0E0",
            fg="#1f2937"
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 30))
        
        
    # SUMMARY CARDS
    def create_summary_cards(self):
        card_frame = tk.Frame(self, bg="#E0E0E0")
        card_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        
        total_products = services.get_total_products()
        total_stock = services.get_total_stock()
        total_inventory_value = services.get_total_inventory_value()
        low_stock_products = services.get_low_stock_products(limit_stock=5)
        
        
        cards = [
            ("Total Produk", total_products),
            ("Total Stok", total_stock),
            ("Nilai Inventori", formatter.format_rupiah(total_inventory_value)),
            ("Produk Stok Menipis", len(low_stock_products))
        ]
        
        for index, card in enumerate(cards):
            title = card[0]
            value = card[1]
        
            self.create_card(
                parent=card_frame,
                title=title,
                value=value,
                column=index
            )
            card_frame.grid_columnconfigure(index, weight=1)
    
    
    # CARD COMPONENT
    def create_card(self, parent, title, value, column):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#b6b6b6",
            highlightthickness=1
        )
        card.grid(row=0, column=column, sticky="nsew", padx=8)

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1f2937"
        )
        title_label.pack(anchor="center", padx=18, pady=(16, 5))

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1f2937"
        )
        value_label.pack(anchor="center", padx=18, pady=(0, 16))

        
    # LOW STOCK SECTION
    def create_low_stock_section(self):
        section = tk.Frame(
            self,
            bg="#f5f7fb",
            highlightbackground="#a7a7a7",
            highlightthickness=1
        )
        section.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        section_title = tk.Label(
            section,
            text="Produk dengan Stok Menipis",
            font=("Arial", 16, "bold"),
            bg="#f5f7fb",
            fg="#1f2937"
        )
        section_title.pack(anchor="w", padx=18, pady=(16, 10))
        
        columns = ("id", "name", "category", "stock", "status")
        
        table = ttk.Treeview(
            section,
            columns=columns,
            show="headings",
            height=5
        )
        
        table.heading("id", text="ID")
        table.heading("name", text="Nama Produk")
        table.heading("category", text="Kategori")
        table.heading("stock", text="Stok")
        table.heading("status", text="Status")
        
        table.column("id", width=60, anchor="center")
        table.column("name", width=260)
        table.column("category",width=260)
        table.column("stock", width=80, anchor="center")
        table.column("status", width=140, anchor="center")
        
        table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        low_stock_products = services.get_low_stock_products(limit_stock=5)
        if len(low_stock_products) == 0:
            table.insert(
                "",
                "end",
                values=("_", "Tidak ada produk dengan stok menipis", "_", "_", "_")
            )
            return
        
        for product in low_stock_products:
            table.insert(
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