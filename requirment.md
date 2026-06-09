# Aplikasi Manajemen Toko GUI

Aplikasi desktop untuk manajemen toko dengan fitur lengkap mencakup produk, promosi, transaksi, dan analitik.

---

# Tech Stack

## Programing language
- Python 3.x

---

## Eksternal library
- **Tkinter** - Kerangka Kerja GUI (bawaan Python)
- **Matplotlib** - Visualisasi data dan pembuatan grafik
- **CSV** - Ekspor dan pelaporan data

---

## Built in Python Library
- `tkinter` - Komponen GUI
- `tkinter.ttk` - Widget bertemat (Treeview, Scrollbar)
- `tkinter.messagebox` - Kotak dialog
- `tkinter.simpledialog` - Dialog input
- `csv` - I/O berkas untuk ekspor data
- `datetime` - Manajemen timestamp
- `json` - Serialisasi data (opsional)

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

# Halaman 1 - Dasbor

### Fitur:
- **Kartu Ringkasan**:
  - Total Produk (jumlah)
  - Total Stok (jumlah stok semua produk)
  - Nilai Inventori (perhitungan nilai stok)
  - Produk Stok Menipis (peringatan stok rendah)

- **Bagian Stok Rendah**:
  - Tabel produk dengan stok ≤ 5 unit
  - Detail: ID, Nama, Kategori, Stok, Status
  - Pembaruan waktu nyata

---

# Halaman 2 - Kelola Produk

### Fitur Utama:
- **Menambahkan Produk**:
  - Input: Nama, Kategori, Harga, Stok
  - Pembuatan ID produk otomatis
  - Validasi data input
  - Penugasan status otomatis

- **Menampilkan Data Produk**:
  - Tabel interaktif dengan scrollbar
  - Kolom: ID, Nama, Kategori, Harga, Stok, Status
  - Format otomatis (Rupiah untuk harga)

- **Mencari Produk**:
  - Pencarian berdasarkan nama atau kategori
  - Penyaringan waktu nyata
  - Atur ulang pencarian

- **Memperbarui Produk**:
  - Perbarui nama, kategori, harga, stok
  - Validasi sebelum pembaruan
  - Penyegaran status otomatis

- **Menghapus Produk**:
  - Konfirmasi penghapusan
  - Penghapusan permanen dari pangkalan data

- **Manajemen Stok**:
  - Tambah Stok (+)
  - Kurangi Stok (-)
  - Validasi ketersediaan stok
  - Pembaruan status otomatis (Tersedia/Stok Menipis/Habis)

---

# Halaman 3 - Kelola Promosi

### Fitur Utama:
- **Menambahkan Promosi**:
  - Pilih produk berdasarkan ID
  - Input persentase diskon (1-100%)
  - Validasi: produk harus ada, tidak ada promosi aktif sebelumnya
  - Perhitungan harga akhir otomatis

- **Menampilkan Promosi**:
  - Tabel promosi dengan detail produk
  - Kolom: ID Promosi, Nama Produk, Kategori, Harga Asli, Diskon %, Harga Akhir, Status
  - Perhitungan harga waktu nyata

- **Mencari Promosi**:
  - Pencarian berdasarkan nama produk atau kategori
  - Filter promosi aktif/tidak aktif
  - Atur ulang pencarian

- **Memperbarui Promosi**:
  - Perbarui persentase diskon
  - Validasi input (1-100%)
  - Perhitungan harga akhir baru otomatis

- **Menghapus Promosi**:
  - Nonaktifkan promosi
  - Konfirmasi penghapusan

- **Riwayat Promosi**:
  - Lacak semua perubahan promosi
  - Log: Aksi, Produk, Diskon Lama/Baru, Status, Stempel Waktu
  - Lihat riwayat lengkap

---

# Halaman 4 - Kelola Transaksi

### Fitur Utama:
- **Informasi Ringkasan**:
  - Transaksi Masuk (jumlah)
  - Transaksi Keluar (jumlah)
  - Total Transaksi (jumlah total)
  - Total Pendapatan (jumlah transaksi keluar)

- **Membuat Transaksi**:
  - Input: Jenis (Masuk/Keluar), ID Produk, Kuantitas
  - Terapkan diskon promosi otomatis jika tersedia
  - Pembaruan stok otomatis
  - Validasi ketersediaan stok untuk Keluar

- **Menampilkan Transaksi**:
  - Tabel lengkap dengan scrollbar horizontal & vertikal
  - Kolom: ID, ID Produk, Nama Produk, Jenis, Jml, Harga Asli, Diskon %, Harga Akhir, Total, Tanggal, Status
  - Format: Rupiah, Persentase, Waktu tanggal

- **Tindakan Toolbar**:
  - **Cek Saldo**: Tampilkan total pendapatan
  - **Ekspor CSV**: Unduh laporan transaksi
  - **Segarkan**: Segarkan tabel & ringkasan

---

# Halaman 5 - Statistik Toko

### Kartu Ringkasan:
- Rata-rata Harga Produk
- Produk Nilai Tertinggi (nilai inventori tertinggi)
- Promosi Aktif (jumlah promosi aktif)
- Total Diskon Diberikan (dari transaksi)
- Total Pendapatan (total revenue)
- Barang Terjual (total item terjual)

### Grafik & Visualisasi:
- **Grafik Produk Paling Laku**: Grafik batang - 5 produk terlaris berdasarkan kuantitas
- **Grafik Produk Pendapatan Teratas**: Grafik batang - 5 produk teratas berdasarkan pendapatan

### Tabel Data:
- **Performa Promosi**: 
  - Kolom: ID Promo, Nama Produk, Diskon %, Terjual, Pendapatan, Total Diskon, Status
  - Diurutkan berdasarkan pendapatan menurun

- **Transaksi Terbaru**:
  - Kolom: ID, Nama Produk, Jenis, Jml, Total, Tanggal, Status
  - 5 transaksi terakhir dalam urutan kronologis terbalik


---

# Arsitektur

## Struktur Folder
```
StoreManagement_GUI/
├── main.py                 # Titik masuk aplikasi
├── data/
│   └── database.py        # Pangkalan data dalam memori
├── services/
│   ├── __init__.py        # Ekspor layanan
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
    └── formatter.py       # Fungsi utilitas (format_rupiah)
```

## Lapisan Layanan
- **Services**: Logika bisnis untuk setiap fitur
- **Database**: Penyimpanan data dalam memori
- **Pages**: Komponen GUI & interaksi pengguna
- **Utils**: Fungsi pembantu

---

# Implementasi Fitur Utama

## Fitur yang Telah Selesai
- ✓ CRUD Produk + Manajemen Stok
- ✓ Manajemen Promosi + Pelacakan Riwayat
- ✓ Pencatatan Transaksi (Masuk/Keluar)
- ✓ Dasbor dengan Kartu Ringkasan
- ✓ Statistik & Analitik Lanjutan
- ✓ Ekspor CSV untuk Transaksi
- ✓ Validasi Data Waktu Nyata
- ✓ Penerapan Diskon Otomatis
- ✓ Notifikasi Stok Rendah
- ✓ Grafik Matplotlib untuk Visualisasi

## Integritas Data
- Validasi input di setiap operasi
- Pemeriksaan ketersediaan stok
- Perhitungan status otomatis
- Pencegahan konflik promosi
- Pencatatan transaksi

---

# Fitur UI/UX

## Skema Warna
- Utama: #1e3a5f (Biru Laut)
- Sekunder: #27496d (Biru)
- Aksen: #2563eb (Biru Cerah)
- Bahaya: #dc2626 (Merah)
- Sukses: #16a34a (Hijau)
- Netral: #6b7280 (Abu-abu)

## Komponen
- Navigasi Sidebar dengan 5 halaman utama
- Tabel Treeview interaktif dengan scrollbar
- Dialog modal untuk input/konfirmasi
- Pembaruan ringkasan waktu nyata
- Tata letak responsif dengan sistem grid

---

# Performa & Batasan

- **Memori**: Penyimpanan dalam memori yang efisien
- **Batas Data**: Tidak terbatas (tergantung RAM yang tersedia)
- **Pengguna Bersamaan**: Hanya pengguna tunggal
- **Sesi**: Data persisten sampai aplikasi ditutup
- **I/O Berkas**: Ekspor CSV didukung

---

# Peningkatan Masa Depan (Opsional)

- Integrasi database (SQLite/MySQL)
- Autentikasi pengguna & peran
- Dukungan multi-pengguna
- Persistensi data antar sesi
- Penyaringan & pelaporan lanjutan
- Notifikasi email
- Versi aplikasi mobile

---