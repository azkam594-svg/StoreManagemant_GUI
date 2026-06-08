import tkinter as tk


def show_statistics_page(parent):
    title = tk.Label(
        parent,
        text="Store Statistics",
        font=("Arial", 24, "bold"),
        bg="#f5f7fb",
        fg="#1f2937"
    )
    title.pack(anchor="w", padx=30, pady=(30, 20))