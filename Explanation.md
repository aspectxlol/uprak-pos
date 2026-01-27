# Penjelasan Lengkap main.py

Dokumen ini menjelaskan setiap bagian dan baris kode dari file `main.py` pada proyek UPRAK-POS agar mudah dipahami oleh semua anggota tim.

---

## 1. Impor Modul (Imports)
Bagian ini mengimpor modul-modul Python yang diperlukan:
- `os`: Untuk operasi sistem seperti membersihkan layar terminal.
- `csv`: Untuk membaca dan menulis file CSV (produk).
- `datetime`: Untuk mendapatkan waktu dan tanggal saat ini (misal, pada struk).

---

## 2. Utilitas Warna Terminal (Color Utility)
Bagian ini berisi:
- Fungsi `color(text, code)`: Memberi warna pada teks di terminal menggunakan kode ANSI.
- Variabel warna seperti `COLOR_HEADER`, `COLOR_MENU`, dll, untuk membedakan tampilan menu, pesan, dan input.

---

## 3. Fungsi Utilitas (Utility Functions)
Fungsi-fungsi umum yang digunakan di seluruh aplikasi:
- `clear_screen()`: Membersihkan layar terminal.
- `pause(msg)`: Menunggu input Enter dari pengguna.
- `input_number(prompt, allow_zero)`: Meminta input angka desimal, validasi agar tidak salah.
- `input_int(prompt, allow_zero)`: Meminta input angka bulat, validasi agar tidak salah.
- `get_timestamp()`: Mengambil waktu dan tanggal saat ini dalam format string.
- `format_idr(amount)`: Mengubah angka menjadi format Rupiah Indonesia (misal: Rp 10.000).

---

## 4. Model Data / Kelas Utama (Data Models / Main Class)
Kelas utama POS yang menyimpan dan mengelola data produk, keranjang, dan transaksi:
- `__init__`: Inisialisasi data produk, keranjang, dan file produk.
- `load_products()`: Membaca data produk dari file CSV ke dalam list.
- `save_products()`: Menyimpan data produk ke file CSV.

---

## 5. Manajemen Produk (Product Management)
Fungsi-fungsi untuk mengelola produk:
- `add_product()`: Menambah produk baru ke sistem, validasi input, dan simpan ke file.
- `edit_product()`: Mengedit produk yang sudah ada berdasarkan ID, validasi input.
- `list_products(show_header)`: Menampilkan daftar produk yang tersedia.

---

## 6. Manajemen Keranjang (Cart Management)
Fungsi-fungsi untuk mengelola keranjang belanja:
- `add_to_cart()`: Menambah produk ke keranjang berdasarkan ID dan jumlah.
- `remove_from_cart()`: Menghapus produk dari keranjang berdasarkan ID.
- `show_cart()`: Menampilkan isi keranjang beserta subtotal dan total harga.

---

## 7. Logika Transaksi (Transaction Logic)
Fungsi untuk proses transaksi:
- `checkout()`: Proses pembayaran, validasi uang yang diterima, hitung kembalian, dan kosongkan keranjang setelah transaksi.

---

## 8. Penanganan Struk (Receipt Handling)
Fungsi untuk membuat dan menyimpan struk transaksi:
- `generate_receipt(total, cash, change)`: Membuat file struk berisi detail transaksi, produk, total, pembayaran, dan kembalian.

---

## 9. Tampilan Menu (Menu Rendering)
Fungsi untuk menampilkan menu utama dan menerima pilihan pengguna:
- `main_menu()`: Menampilkan menu utama dan mengembalikan pilihan pengguna.

---

## 10. Loop Utama (Main Loop)
Bagian utama yang menjalankan aplikasi secara terus-menerus:
- `main()`: Menjalankan aplikasi POS, memanggil fungsi sesuai pilihan pengguna, dan keluar jika dipilih.
- `if __name__ == "__main__": main()`: Menjalankan aplikasi jika file ini dieksekusi langsung.

---

# Penjelasan Baris per Baris

Setiap fungsi di atas sudah dijelaskan secara singkat. Untuk penjelasan lebih detail per baris, silakan lihat komentar di dalam kode atau tanyakan bagian spesifik yang ingin dipahami lebih dalam.

Jika ada bagian kode yang membingungkan, silakan diskusikan di tim!
