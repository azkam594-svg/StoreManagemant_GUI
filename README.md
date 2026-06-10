# Aplikasi Manajemen Toko GUI

Aplikasi desktop untuk manajemen toko dengan fitur mencakup produk, promosi, transaksi, dan analitik.

---

# Jenis Aplikasi

- **GUI** (Antarmuka Pengguna Grafis) - Aplikasi Desktop
- **Aplikasi Offline** - Tidak memerlukan internet
- **Penyimpanan Dalam Memori** - Data disimpan di RAM (persisten per sesi)
- **Pengguna Tunggal** - Aplikasi untuk satu pengguna
- **Lintas Platform** - Berjalan di Windows, macOS, Linux

---

# Fitur Utama

## 1. Dasbor
- Ringkasan informasi toko
- Total produk, total stok, nilai inventori
- Notifikasi produk stok menipis
- Ikhtisar cepat untuk pemantauan

## 2. Manajemen Produk
- Operasi CRUD untuk produk
- Manajemen stok (tambah/kurangi)
- Pencarian dan filter produk
- Pelacakan status otomatis

## 3. Manajemen Promosi
- Buat dan kelola promosi produk
- Pelacakan diskon dan riwayat
- Analitik performa promosi
- Perhitungan harga otomatis dengan diskon

## 4. Manajemen Transaksi
- Catat transaksi masuk/keluar
- Tampilkan riwayat transaksi
- Pemeriksaan saldo
- Ekspor CSV untuk pelaporan

## 5. Statistik & Analitik Toko
- Dasbor komprehensif dengan kartu ringkasan
- Grafik performa penjualan (kuantitas & pendapatan)
- Analisis efektivitas promosi
- Pelacakan produk paling laku
- Pemantauan transaksi terbaru

---

# Arsitektur

## Struktur Folder
```
StoreManagement_GUI/
├── main.py                
├── data/
│   └── database.py        
├── services/
│   ├── __init__.py       
│   ├── products_service.py
│   ├── promotions_service.py
│   ├── transactions_service.py
│   └── statistic_service.py
├── pages/
│   ├── dashboard_page.py
│   ├── products_page.py
│   ├── promotions_page.py
│   ├── transactions_page.py
│   └── statistics_page.py
└── utils/
    ├── __init__.py
    └── formatter.py       
```