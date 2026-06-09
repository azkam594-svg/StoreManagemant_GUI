import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from utils.formatter import format_rupiah
import services



# SHOWING TO MAIN
def show_promotions_page(parent):
    page = PromotionsPage(parent)
    page.pack(fill="both", expand=True)
    



# PROMOTION PAGE 
class PromotionsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#E9E9E9")
        
        self.search_var = tk.StringVar()
        
        self.create_header()
        self.create_toolbar()
        self.create_table()
        
        self.load_promotions()
    

    #  HEADER
    def create_header(self,):
        title = tk.Label(
            self,
            text="Manage Promotions",
            font=("Arial", 24, "bold"),
            bg="#E9E9E9",
            fg="#1f2937"
        )
        title.pack(anchor="w", padx=30, pady=(30, 15))
        
    # BUTTON  
    def create_toolbar(self):
        """
        membuat area tombol
        - search
        - reset
        - tambah
        - edit
        - hapus
        - Riwayat promosi
        """
        
        toolbar = tk.Frame(self, bg="#E9E9E9")
        toolbar.pack(fill="x", padx=30, pady=(0, 10))
        
        
        # input search
        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Arial", 11),
            width=30
        )
        search_entry.pack(side="left", padx=(0, 8), ipadx=5)
        
        
        # Search Button
        search_button = tk.Button(
            toolbar,
            text="Cari",
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.search_promotion
        )
        search_button.pack(side="left", padx=4)
        
        
        # Reset Button
        reset_button = tk.Button(
            toolbar,
            text="Reset",
            bg="#6b7280",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.reset_search
        )
        reset_button.pack(side="left", padx=4)
    
    
        # Add Button
        add_button = tk.Button(
            toolbar,
            text="+ Tambah Promo",
            bg="#16a34a",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.open_add_form
        )
        add_button.pack(side="right", padx=4)
        
        
        # Edit Button
        edit_button = tk.Button(
            toolbar,
            text="Edit",
            bg="#f59e0b",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.open_edit_form
        )
        edit_button.pack(side="right", padx=4)

        
        # Delete Button
        delete_button = tk.Button(
            toolbar,
            text="Hapus",
            font=("Arial", 10),
            bg="#C50707",
            fg="white",
            command=self.delete_selected_promotion
        )
        delete_button.pack(side="right", padx=4)
        
        
        # PromotionHistories
        history_button = tk.Button(
            toolbar,
            text="Riwayat Promosi",
            font=("Arial", 10),
            bg="#84BD00",
            fg="white",
            command= self.open_promotion_history
        )
        history_button.pack(side="right", padx= 5)
        
    
    # TABEL
    def create_table(self):
        table_container = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d1d5db",
            highlightthickness=1
        )
        table_container.pack(fill="both", expand=True, padx=30, pady=15)
        
        columns = (
            "id",
            "product_name",
            "category",
            "original_price",
            "discount_percent",
            "final_price",
            "status"
        )
        
        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )
        
        # Heading kolom
        self.table.heading("id", text="ID")
        self.table.heading("product_name", text="Nama Produk")
        self.table.heading("category", text="Kategori")
        self.table.heading("original_price", text="Harga Asli")
        self.table.heading("discount_percent", text="Diskon")
        self.table.heading("final_price", text="Harga Setelah Diskon")
        self.table.heading("status", text="Status")
        
        
        # Ukuran kolom
        self.table.column("id", width=50, anchor="center")
        self.table.column("product_name", width=220)
        self.table.column("category", width=140, anchor="center")
        self.table.column("original_price", width=140, anchor="center")
        self.table.column("discount_percent", width=90, anchor="center")
        self.table.column("final_price", width=170, anchor="center")
        self.table.column("status", width=120, anchor="center")
        
        # scrollbar
        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )
        
        self.table.configure(yscrollcommand=scrollbar.set)
        
        self.table.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)
    
    
    
    # load data ke tabel
    def load_promotions(self, promotion_list=None):
        
        # delete isi tabel lama
        for item in self.table.get_children():
            self.table.delete(item)
            
        
        if promotion_list is None:
            promotion_list = services.get_all_promotions()
            
        for promotion in promotion_list:
            self.table.insert(
                "",
                "end",
                values=(
                    promotion["id"],
                    promotion["product_name"],
                    promotion["category"],
                    format_rupiah(promotion["original_price"]),
                    f"{promotion['discount_percent']}%",
                    format_rupiah(promotion["final_price"]),
                    promotion["status"]
                )
            )
            
    # warning selected promotion
    def get_selected_promotion_id(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showwarning(
                "Pilih Produk",
                "Pilih salah satu produk terlebih dahulu."
            )
            return None

        item_values = self.table.item(selected_item[0], "values")
        promotion_id = item_values[0]

        return promotion_id
            
            
    
# BUTTON CALLBACK
    
    # search
    def search_promotion(self):
        keyword = self.search_var.get()
        result = services.search_promotions(keyword)
        self.load_promotions(result)
        
    # reset
    def reset_search(self):
        self.search_var.set("")
        self.load_promotions()
        
    
    # add
    def open_add_form(self): 
        PromotionForm(
            master=self,
            mode="add",
            promotion=None,
            on_success=self.load_promotions
        )


    # edit 
    def open_edit_form(self):
        promotion_id = self.get_selected_promotion_id()

        if promotion_id is None:
            return

        success, result = services.get_promotion_by_id(promotion_id)

        if not success:
            messagebox.showerror("Error", result)
            return

        promotion = result

        PromotionForm(
            master=self,
            mode="edit",
            promotion=promotion,
            on_success=self.load_promotions
        )


    # delete
    def delete_selected_promotion(self):
        promotion_id = self.get_selected_promotion_id()

        if promotion_id is None:
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus promosi ID {promotion_id}?"
        )
        
        if not confirm:
            return

        success, result = services.delete_promotion(promotion_id)

        if success:
            messagebox.showinfo("Berhasil", result)
            self.load_promotions()
        else:
            messagebox.showerror("Gagal", result)
            return
        
    # Riwayat promosi
    def open_promotion_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Riwayat Promosi")
        history_window.geometry("900x400")
        history_window.resizable(False, False)
        
        title_label = tk.Label(
        history_window,
        text="Riwayat Promosi",
        font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        columns = (
            "id",
            "promotion_id",
            "product_id",
            "action",
            "old_discount",
            "new_discount",
            "status",
            "created_at"
        )

        history_table = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

        history_table.heading("id", text="ID")
        history_table.heading("promotion_id", text="ID Promosi")
        history_table.heading("product_id", text="ID Produk")
        history_table.heading("action", text="Aksi")
        history_table.heading("old_discount", text="Diskon Lama")
        history_table.heading("new_discount", text="Diskon Baru")
        history_table.heading("status", text="Status")
        history_table.heading("created_at", text="Tanggal")

        history_table.column("id", width=50, anchor="center")
        history_table.column("promotion_id", width=100, anchor="center")
        history_table.column("product_id", width=100, anchor="center")
        history_table.column("action", width=100, anchor="center")
        history_table.column("old_discount", width=120, anchor="center")
        history_table.column("new_discount", width=120, anchor="center")
        history_table.column("status", width=100, anchor="center")
        history_table.column("created_at", width=180, anchor="center")

        history_table.pack(fill="both", expand=True, padx=10, pady=10)

        histories = services.get_all_promotion_histories()

        for history in histories:
            history_table.insert(
                "",
                "end",
                values=(
                    history["id"],
                    history["promotion_id"],
                    history["product_id"],
                    history["action"],
                    f'{history["old_discount"]}%',
                    f'{history["new_discount"]}%',
                    history["status"],
                    history["created_at"]
                )
            )
        
        
        
        
# PROMOTION FORM
class PromotionForm(tk.Toplevel):

    def __init__(self, master, mode, promotion, on_success):
        super().__init__(master)

        self.master = master
        self.mode = mode
        self.promotion = promotion
        self.on_success = on_success

        if self.mode == "add":
            self.title("Tambah Promo")
        else:
            self.title("Edit Promo")

        self.geometry("520x300")
        self.resizable(False, False)
        self.configure(bg="#f5f7fb")

        # Membuat form muncul di atas window utama
        self.transient(master.winfo_toplevel())

        # Membuat user harus menyelesaikan form dulu sebelum klik window utama
        self.grab_set()

        self.create_form()

        if self.mode == "edit" and self.promotion is not None:
            self.fill_form_data()


    # CREATE FORM
    def create_form(self):
        """
        Membuat form input promosi:
        - ID Produk
        - Persentase Diskon
        """

        title_text = "Tambah Promo" if self.mode == "add" else "Edit Promo"

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


        # ID Produk
        tk.Label(
            form_frame,
            text="ID Produk",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.product_id_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.product_id_entry.pack(fill="x", pady=(4, 10), ipady=5)


        # Persentase Diskon
        tk.Label(
            form_frame,
            text="Persentase Diskon",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb"
        ).pack(anchor="w")

        self.discount_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.discount_entry.pack(fill="x", pady=(4, 10), ipady=5)


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
            command=self.save_promotion
        )
        save_button.pack(side="right", padx=5)


    # FILL EDIT FORM
    def fill_form_data(self):
        self.product_id_entry.insert(0, self.promotion["product_id"])
        self.discount_entry.insert(0, self.promotion["discount_percent"])

        # Saat edit, ID produk tidak boleh diubah
        self.product_id_entry.config(state="disabled")
        

    # SAVE PROMOTION
    def save_promotion(self):
        product_id = self.product_id_entry.get()
        discount_percent = self.discount_entry.get()

        if self.mode == "add":
            success, result = services.add_promotion(
                product_id=product_id,
                discount_percent=discount_percent
            )
        else:
            success, result = services.update_promotion(
                promotion_id=self.promotion["id"],
                discount_percent=discount_percent
            )

        if success:
            messagebox.showinfo(
                "Berhasil",
                "Data promosi berhasil disimpan."
            )

            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Gagal", result)