import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import services
from utils.formatter import format_rupiah



# SHOWING TO MAAIN
def show_products_page(parent):
    page = ProductPage(parent)
    page.pack(fill="both", expand=True)


# PRODUCT PAGE
class ProductPage(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent, bg="#E9E9E9")

        # Variable untuk menyimpan keyword pencarian
        self.search_var = tk.StringVar()

        self.create_header()
        self.create_toolbar()
        self.create_table()

        self.load_products()


    # HEADER
    def create_header(self):
        title = tk.Label(
            self,
            text="Manage Products",
            font=("Arial", 24, "bold"),
            bg="#E9E9E9",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=30, pady=(30, 15))

    # TOOLBAR BUTTON
    def create_toolbar(self):
        """
        Membuat area tombol:
        - Search
        - Reset
        - Tambah
        - Edit
        - Hapus
        - Tambah Stok
        - Kurangi Stok
        """

        toolbar = tk.Frame(self, bg="#E9E9E9")
        toolbar.pack(fill="x", padx=30, pady=(0, 10))

        # Input pencarian
        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Arial", 11),
            width=30
        )
        search_entry.pack(side="left", padx=(0, 8), ipady=5)

        # Tombol Search
        search_button = tk.Button(
            toolbar,
            text="Cari",
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.search_product
        )
        search_button.pack(side="left", padx=4)

        # Tombol Reset
        reset_button = tk.Button(
            toolbar,
            text="Reset",
            bg="#6b7280",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.reset_search
        )
        reset_button.pack(side="left", padx=4)

        # Tombol Hapus Produk
        delete_button = tk.Button(
            toolbar,
            text="Hapus",
            bg="#dc2626",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.delete_selected_product
        )
        delete_button.pack(side="right", padx=4)

        # Tombol Edit Produk
        edit_button = tk.Button(
            toolbar,
            text="Edit",
            bg="#f59e0b",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.open_edit_form
        )
        edit_button.pack(side="right", padx=4)

        # Tombol Tambah Produk
        add_button = tk.Button(
            toolbar,
            text="+ Tambah Produk",
            bg="#16a34a",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.open_add_form
        )
        add_button.pack(side="right", padx=4)

        # Tombol Kurangi Stok
        decrease_stock_button = tk.Button(
            toolbar,
            text="- Stok",
            bg="#7c2d12",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.decrease_stock
        )
        decrease_stock_button.pack(side="right", padx=4)

        # Tombol Tambah Stok
        increase_stock_button = tk.Button(
            toolbar,
            text="+ Stok",
            bg="#0f766e",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.increase_stock
        )
        increase_stock_button.pack(side="right", padx=4)




    # = TABLE
    def create_table(self):
        table_container = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d1d5db",
            highlightthickness=1
        )
        table_container.pack(fill="both", expand=True, padx=30, pady=15)

        columns = ("id", "name", "category", "price", "stock", "status")

        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )

        # Heading kolom
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Nama Produk")
        self.table.heading("category", text="Kategori")
        self.table.heading("price", text="Harga")
        self.table.heading("stock", text="Stok")
        self.table.heading("status", text="Status")

        # Ukuran kolom
        self.table.column("id", width=50, anchor="center")
        self.table.column("name", width=250)
        self.table.column("category", width=150)
        self.table.column("price", width=150, anchor="center")
        self.table.column("stock", width=80, anchor="center")
        self.table.column("status", width=130, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

    # LOAD DATA PRODUK ke TABEL
    def load_products(self, product_list=None):
       
        # Hapus semua isi tabel lama
        for item in self.table.get_children():
            self.table.delete(item)

        # Ambil data produk dari service
        if product_list is None:
            product_list = services.get_all_products()

        # Masukkan data ke tabel
        for product in product_list:
            self.table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["name"],
                    product["category"],
                    format_rupiah(product["price"]),
                    product["stock"],
                    product["status"]
                )
            )



# BUTTON CALLBACK

    # = SEARCH PRODUCT
    def search_product(self):
        keyword = self.search_var.get()
        
        result = services.search_products(keyword)
        
        self.load_products(result)
        
        
    # RESET SEARCH
    def reset_search(self):
        self.search_var.set("")
        self.load_products()
        
        

    # GET SELECTED PRODUCT ID
    def get_selected_product_id(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showwarning(
                "Pilih Produk",
                "Pilih salah satu produk terlebih dahulu."
            )
            return None

        item_values = self.table.item(selected_item[0], "values")

        product_id = item_values[0]

        return product_id



    # = ADD PRODUCT
    def open_add_form(self): 
        ProductForm(
            master=self,
            mode="add",
            product=None,
            on_success=self.load_products
        )


    # = EDIT PRODUCT
    def open_edit_form(self):
        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        success, result = services.get_product_by_id(product_id)

        if not success:
            messagebox.showerror("Error", result)
            return

        product = result

        ProductForm(
            master=self,
            mode="edit",
            product=product,
            on_success=self.load_products
        )
    
    
    # = DELETE PRODUCT
    def delete_selected_product(self):
        """
        Menghapus produk yang dipilih dari tabel.

        Function ini memanggil:
            services.delete_product(product_id)
        """

        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        success, result = services.get_product_by_id(product_id)

        if not success:
            messagebox.showerror("Error", result)
            return

        product = result

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah kamu yakin ingin menghapus produk '{product['name']}'?"
        )

        if not confirm:
            return

        success, result = services.delete_product(product_id)

        if success:
            messagebox.showinfo("Berhasil", result)
            self.load_products()
        else:
            messagebox.showerror("Gagal", result)


    # = TAMBAH STOCK
    def increase_stock(self):
        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        quantity = simpledialog.askinteger(
            "Tambah Stok",
            "Masukkan jumlah stok yang ingin ditambahkan:",
            minvalue=1
        )

        if quantity is None:
            return

        success, result = services.increase_product_stock(product_id, quantity)

        if success:
            messagebox.showinfo("Berhasil", "Stok produk berhasil ditambahkan.")
            self.load_products()
        else:
            messagebox.showerror("Gagal", result)

    
    # = KURANGI STOCK
    def decrease_stock(self):
        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        quantity = simpledialog.askinteger(
            "Kurangi Stok",
            "Masukkan jumlah stok yang ingin dikurangi:",
            minvalue=1
        )

        if quantity is None:
            return

        success, result = services.decrease_product_stock(product_id, quantity)

        if success:
            messagebox.showinfo("Berhasil", "Stok produk berhasil dikurangi.")
            self.load_products()
        else:
            messagebox.showerror("Gagal", result)



# PRODUCT FORM 
class ProductForm(tk.Toplevel):

    def __init__(self, master, mode, product, on_success):
        super().__init__(master)

        self.master = master
        self.mode = mode
        self.product = product
        self.on_success = on_success

        if self.mode == "add":
            self.title("Tambah Produk")
        else:
            self.title("Edit Produk")

        self.geometry("520x400")
        self.resizable(False, False)
        self.configure(bg="#f5f7fb")

        self.transient(master.winfo_toplevel())

        self.grab_set()

        self.create_form()

        if self.mode == "edit" and self.product is not None:
            self.fill_form_data()

    
    # CREATE FORM
    def create_form(self):
        """
        Membuat field input:
        - Nama produk
        - Kategori
        - Harga
        - Stok
        """

        title_text = "Tambah Produk" if self.mode == "add" else "Edit Produk"

        title = tk.Label(
            self,
            text=title_text,
            font=("Arial", 18, "bold"),
            bg="#f5f7fb",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=25, pady=(20, 15))

        form_frame = tk.Frame(self, bg="#f5f7fb")
        form_frame.pack(fill="x", padx=25)

        # Nama produk
        tk.Label(
            form_frame,
            text="Nama Produk",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.name_entry = tk.Entry(form_frame, font=("Arial", 11))
        self.name_entry.pack(fill="x", pady=(4, 10), ipady=5)

        # Kategori
        tk.Label(
            form_frame,
            text="Kategori",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.category_entry = tk.Entry(form_frame, font=("Arial", 11))
        self.category_entry.pack(fill="x", pady=(4, 10), ipady=5)

        # Harga
        tk.Label(
            form_frame,
            text="Harga",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.price_entry = tk.Entry(form_frame, font=("Arial", 11))
        self.price_entry.pack(fill="x", pady=(4, 10), ipady=5)

        # Stok
        tk.Label(
            form_frame,
            text="Stok",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.stock_entry = tk.Entry(form_frame, font=("Arial", 11))
        self.stock_entry.pack(fill="x", pady=(4, 10), ipady=5)

        # Button frame
        button_frame = tk.Frame(self, bg="#f5f7fb")
        button_frame.pack(fill="x", padx=25, pady=15)

        cancel_button = tk.Button(
            button_frame,
            text="Batal",
            bg="#6b7280",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            command=self.destroy
        )
        cancel_button.pack(side="right", padx=5)

        save_button = tk.Button(
            button_frame,
            text="Simpan",
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            command=self.save_product
        )
        save_button.pack(side="right", padx=5)

    
    # FILL EDIT FORM
    def fill_form_data(self):
        self.name_entry.insert(0, self.product["name"])
        self.category_entry.insert(0, self.product["category"])
        self.price_entry.insert(0, self.product["price"])
        self.stock_entry.insert(0, self.product["stock"])

    
    # SAVE PRODUCT
    def save_product(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if self.mode == "add":
            success, result = services.add_product(
                name=name,
                category=category,
                price=price,
                stock=stock
            )
        else:
            success, result = services.update_product(
                product_id=self.product["id"],
                name=name,
                category=category,
                price=price,
                stock=stock
            )

        if success:
            messagebox.showinfo("Berhasil", "Data produk berhasil disimpan.")

            # Tutup popup
            self.destroy()

            # Refresh tabel di halaman produk
            self.on_success()
        else:
            messagebox.showerror("Gagal", result)