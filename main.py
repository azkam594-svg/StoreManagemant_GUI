import tkinter as tk
from tkinter import messagebox

# Import Folder Pages
from pages.dashboard_page import show_dashboard_page
from pages.products_page import show_products_page
from pages.promotions_page import show_promotions_page
from pages.transactions_page import show_transactions_page
from pages.statistics_page import show_statistics_page


# CLEAR DEFAULT WIDGET
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# MOVE PAGE
def change_page(page_function):
    # Hapus isi halaman sebelumnya.
    clear_content()
    page_function(content_frame)

# MAIN WINDOW
root = tk.Tk()
root.title("Application Store Management")
root.geometry("1100x650")  # Format: "lebarxtinggi"
root.minsize(900, 550)  # Ukuran minimum window.
root.configure(bg="#f5f7fb")


# CONTENT (Dashboard, Products, Promotions, etc)
content_frame = tk.Frame(
    root,
    bg="#f5f7fb"
)
content_frame.pack(side="right", fill="both", expand=True)





# SIDEBAR MENU
def create_sidebar_button(text, command):
    button = tk.Button(
        sidebar,

        # Tulisan pada tombol.
        text=text,

        # Font tombol.
        font=("Arial", 11, "bold"),

        # Warna tombol.
        bg="#27496d",

        # Warna teks tombol.
        fg="white",

        # Warna saat tombol ditekan / aktif.
        activebackground="#2563eb",
        activeforeground="white",

        # relief="flat" membuat tombol terlihat lebih modern
        # karena tidak memakai border 3D bawaan Tkinter.
        relief="flat",

        # Ukuran tombol.
        width=20,
        height=2,

        # Fungsi yang dijalankan saat tombol diklik.
        command=command
    )
    button.pack(pady=7, padx=20)
    return button

# SIDEBAR
sidebar = tk.Frame(
    root,
    bg="#1e3a5f",
    width=230
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

sidebar_title = tk.Label(
    sidebar,

    text="STORE\nMANAGEMENT",
    font=("Arial", 20, "bold"),
    bg="#1e3a5f",
    fg="white"
)
sidebar_title.pack(pady=(40, 30))

create_sidebar_button(
    "Dashboard",
    lambda: change_page(show_dashboard_page)
)

create_sidebar_button(
    "Manage Products",
    lambda: change_page(show_products_page)
)

create_sidebar_button(
    "Manage Promotions",
    lambda: change_page(show_promotions_page)
)

create_sidebar_button(
    "Manage Transactions",
    lambda: change_page(show_transactions_page)
)

create_sidebar_button(
    "Store Statistics",
    lambda: change_page(show_statistics_page)
)




# EXIT
def exit_app():
    # Popup masagebox untuk konfirmasi keluar aplikasi.
    confirm = messagebox.askyesno(
        "Konfirmasi Keluar",
        "Apakah kamu yakin ingin keluar dari aplikasi?"
    )
    if confirm:
        root.destroy()
  
  
# EXIT BUTTON
exit_button = tk.Button(
    sidebar,
    text="Exit",
    font=("Arial", 11, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    width=20,
    height=2,
    command=exit_app
)
exit_button.pack(side="bottom", pady=30, padx=20) # Menempatkan tombol Exit di bagian bawah sidebar.



# MAIN PAGE
change_page(show_dashboard_page)

root.mainloop()