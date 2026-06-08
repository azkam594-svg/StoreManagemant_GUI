# Store Management GUI

---

# Tech Stack

## Programming Language
- Python

---

## External Library
- Matplotlib
- Tikinter

---

## Built-in Python Library
- datetime
- os
- json

---

# Application Type

- CLI (Command Line Interface)
- Offline Application
- Local Storage
- Single User

---

# Main Feature

## 1. Management Product
## 2. Management Promotion
## 3. Management Finance
## 4. Store analytic

---

# Menu 1 - Product Management

- Menambahkan data barang
- Menampilkan seluruh informasi barang yang tersedia 
- Mencari barang berdasarkan SKU
- Mengupdate barang:
  - Update nama barang
  - Update harga barang
  - Update stock barang
  - Update seluruh data barang
- Menghapus barang berdasarkan SKU

---

# Menu 2 - Promotion Management

- Menambahkan diskon product
  - Input SKU product yang akan di diskon
  - Input persentase diskon
- Menghapus diskon product
- Mengupdate Promosi
- Melihat seluruh product yang sedang diskon
  - Menampilkan harga asli dan harga setelah diskon
  - Menampilkan product dengan diskon terbesar

---

# Menu 3 -  transation management 

- Melihat transation masuk dan keluar total transation
- Mengecek saldo store
- unduh laporan keuangan csv
- riwayat transaction


---

# menu 4 - Store analytik
- Menampilkan Total product
- Menampilkan product paling laku
- Menampilkan product dengan stock hampir habis
- Menampilkan grafik penjualan menggunakan matplotlib
- Menampilkan grafik penghasilan menggunakan matplotlib





# Data Structure
## Product Data

```python
{
    "sku": "P001",
    "name": "Keyboard",
    "price": 150000,
    "stock": 10,
    "discount": 0
}