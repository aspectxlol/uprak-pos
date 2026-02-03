
# =========================================================
# Impor Modul (Imports)
# ---------------------------------------------------------
# Bagian ini mengimpor modul-modul Python yang diperlukan
# untuk menjalankan aplikasi POS, seperti modul file, CSV,
# dan waktu.
# =========================================================
import os
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
	import qrcode
except ImportError:
	subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "-q"])
	import qrcode

# =========================================================
# Utilitas Warna Terminal (Color Utility)
# ---------------------------------------------------------
# Bagian ini berisi fungsi dan variabel untuk memberikan
# warna pada teks di terminal, sehingga tampilan lebih
# mudah dibaca dan menarik.
# =========================================================
def color(text: str, code: str) -> str:
	"""Pembungkus untuk kode warna ANSI di terminal."""
	return f"\033[{code}m{text}\033[0m"

# Kode warna untuk kemudahan penggunaan
COLOR_HEADER = '96'   # Bright cyan
COLOR_MENU = '93'     # Bright yellow
COLOR_OK = '92'       # Bright green
COLOR_ERROR = '91'    # Bright red
COLOR_INPUT = '94'    # Bright blue
COLOR_RESET = '0'

# =========================================================
# Fungsi Utilitas (Utility Functions)
# ---------------------------------------------------------
# Bagian ini berisi fungsi-fungsi utilitas umum seperti
# membersihkan layar, menunggu input pengguna, dan validasi
# input angka. Fungsi-fungsi ini membantu interaksi pengguna
# menjadi lebih nyaman dan aman dari kesalahan input.
# =========================================================
def clear_screen() -> None:
	"""Membersihkan layar terminal untuk tampilan yang lebih rapi."""
	os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg: str = "Tekan Enter untuk melanjutkan...") -> None:
	"""Menghentikan eksekusi sampai pengguna menekan Enter."""
	input(color(msg, COLOR_INPUT))

def input_number(prompt: str, allow_zero: bool = False) -> float:
	"""Meminta pengguna memasukkan angka dan terus meminta sampai input valid."""
	while True:
		val = input(prompt)
		try:
			num = float(val)
			if not allow_zero and num <= 0:
				print("Masukkan angka yang positif.")
				continue
			return num
		except ValueError:
			print("Masukan tidak valid. Masukkan angka.")

def input_int(prompt: str, allow_zero: bool = False) -> int:
	"""Meminta pengguna memasukkan bilangan bulat dan terus meminta sampai input valid."""
	while True:
		val = input(prompt)
		try:
			num = int(val)
			if not allow_zero and num <= 0:
				print("Masukkan bilangan bulat yang positif.")
				continue
			return num
		except ValueError:
			print("Masukan tidak valid. Masukkan bilangan bulat.")

def get_timestamp() -> str:
	"""Mengembalikan tanggal dan waktu saat ini."""
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_idr(amount: float) -> str:
	"""Memformat angka menjadi Rupiah Indonesia (IDR)."""
	return f"Rp {int(amount):,}".replace(",", ".")

# =========================================================
# Model Data / Kelas Utama (Data Models / Main Class)
# ---------------------------------------------------------
# Bagian utama aplikasi POS. Kelas POS menyimpan data produk,
# keranjang belanja, dan mengelola seluruh logika utama
# seperti menambah produk, transaksi, dan pembuatan struk.
# =========================================================
class POS:
	"""Kelas POS utama untuk mengelola produk, keranjang belanja, dan transaksi."""
	def __init__(self) -> None:
		self.products = []  # List produk: {id, name, price}
		self.cart = []      # List keranjang: {id, name, price, qty}
		self.next_product_id = 1
		self.products_file = "products.csv"
		self.load_products()

	def load_products(self) -> None:
		"""Memuat produk dari file CSV jika ada."""
		try:
			with open(self.products_file, newline='', encoding='utf-8') as f:
				reader = csv.DictReader(f)
				self.products = []
				max_id = 0
				for row in reader:
					prod = {
						'id': int(row['id']),
						'name': row['name'],
						'price': float(row['price'])
					}
					self.products.append(prod)
					if prod['id'] > max_id:
						max_id = prod['id']
				self.next_product_id = max_id + 1
		except FileNotFoundError:
			self.products = []
			self.next_product_id = 1

	def save_products(self) -> None:
		"""Menyimpan semua produk ke file CSV."""
		with open(self.products_file, 'w', newline='', encoding='utf-8') as f:
			writer = csv.DictWriter(f, fieldnames=['id', 'name', 'price'])
			writer.writeheader()
			for p in self.products:
				writer.writerow({'id': p['id'], 'name': p['name'], 'price': p['price']})

	# =========================================================
	#  Manajemen Produk (Product Management)
	# ---------------------------------------------------------
	# Bagian ini berisi fungsi-fungsi untuk menambah, mengedit,
	# dan menampilkan daftar produk yang tersedia di sistem POS.
	# =========================================================
	def add_product(self) -> None:
		"""Menambahkan produk baru ke daftar dan menyimpan ke file."""
		clear_screen()
		print(color("=== Tambah Produk ===", COLOR_HEADER))
		print(color("Ketik 'b' atau 'B' untuk membatalkan dan kembali ke menu utama.", COLOR_INPUT))
		name: str = input("Nama produk: ").strip()
		if name.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		price_input: str = input("Harga produk: ")
		if price_input.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		try:
			price = float(price_input)
			if price <= 0:
				print(color("Masukkan harga yang positif.", COLOR_ERROR))
				pause()
				return
		except ValueError:
			print(color("Masukan tidak valid. Masukkan angka.", COLOR_ERROR))
			pause()
			return
		product = {
			'id': self.next_product_id,
			'name': name,
			'price': price
		}
		self.products.append(product)
		self.next_product_id += 1
		self.save_products()
		print(color(f"Produk '{name}' berhasil ditambahkan dengan ID {product['id']}", COLOR_OK))
		pause()

	def edit_product(self) -> None:
		"""Mengedit produk yang ada dengan ID dan menyimpan ke file."""
		clear_screen()
		print(color("=== Edit Produk ===", COLOR_HEADER))
		if not self.products:
			print(color("Tidak ada produk untuk diedit.", COLOR_ERROR))
			pause()
			return
		self.list_products()
		print(color("Ketik 'b' atau 'B' untuk membatalkan dan kembali ke menu utama.", COLOR_INPUT))
		pid_input: str = input("Masukkan ID produk untuk diedit: ").strip()
		if pid_input.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		try:
			pid = int(pid_input)
		except ValueError:
			print(color("Masukan tidak valid. Masukkan bilangan bulat.", COLOR_ERROR))
			pause()
			return
		product = next((p for p in self.products if p['id'] == pid), None)
		if not product:
			print(color("Produk tidak ditemukan.", COLOR_ERROR))
			pause()
			return
		print(f"Mengedit '{product['name']}' (ID {product['id']})")
		new_name: str = input(f"Nama baru (kosongkan untuk tetap '{product['name']}'): ").strip()
		if new_name.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		if new_name:
			product['name'] = new_name
		new_price: str = input(f"Harga baru (kosongkan untuk tetap {product['price']}): ").strip()
		if new_price.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		if new_price:
			try:
				product['price'] = float(new_price)
			except ValueError:
				print(color("Harga tidak valid. Tetap menggunakan harga lama.", COLOR_ERROR))
		self.save_products()
		print(color("Produk berhasil diperbarui.", COLOR_OK))
		pause()

	def list_products(self, show_header=True) -> None:
		"""Menampilkan semua produk yang tersedia."""
		if show_header:
			print(color("ID  Nama                 Harga (IDR)", COLOR_MENU))
			print(color("--  -------------------- -----------", COLOR_MENU))
		for p in self.products:
			print(f"{p['id']:2}  {p['name'][:20]:20} {format_idr(p['price']):>13}")

	# =========================================================
	# Manajemen Keranjang (Cart Management)
	# ---------------------------------------------------------
	# Bagian ini mengatur keranjang belanja, termasuk menambah
	# produk ke keranjang, menghapus produk, dan menampilkan isi
	# keranjang sebelum checkout.
	# =========================================================
	def add_to_cart(self) -> None:
		"""Menambahkan produk ke keranjang berdasarkan ID dan jumlah."""
		clear_screen()
		print(color("=== Tambah ke Keranjang ===", COLOR_HEADER))
		if not self.products:
			print(color("Tidak ada produk yang tersedia.", COLOR_ERROR))
			pause()
			return
		self.list_products()
		print(color("Ketik 'b' atau 'B' untuk membatalkan dan kembali ke menu utama.", COLOR_INPUT))
		pid_input: str = input("Masukkan ID produk untuk ditambahkan: ").strip()
		if pid_input.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		try:
			pid = int(pid_input)
		except ValueError:
			print(color("Masukan tidak valid. Masukkan bilangan bulat.", COLOR_ERROR))
			pause()
			return
		product = next((p for p in self.products if p['id'] == pid), None)
		if not product:
			print(color("Produk tidak ditemukan.", COLOR_ERROR))
			pause()
			return
		qty_input: str = input("Jumlah: ").strip()
		if qty_input.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		try:
			qty = int(qty_input)
			if qty <= 0:
				print(color("Masukkan bilangan bulat yang positif.", COLOR_ERROR))
				pause()
				return
		except ValueError:
			print(color("Masukan tidak valid. Masukkan bilangan bulat.", COLOR_ERROR))
			pause()
			return
		# Check if already in cart
		cart_item = next((c for c in self.cart if c['id'] == pid), None)
		if cart_item:
			cart_item['qty'] += qty
		else:
			self.cart.append({
				'id': product['id'],
				'name': product['name'],
				'price': product['price'],
				'qty': qty
			})
		print(color(f"Berhasil menambahkan {qty} x {product['name']} ke keranjang.", COLOR_OK))
		pause()

	def remove_from_cart(self) -> None:
		"""Menghapus item dari keranjang berdasarkan ID produk."""
		clear_screen()
		print(color("=== Hapus dari Keranjang ===", COLOR_HEADER))
		if not self.cart:
			print(color("Keranjang kosong.", COLOR_ERROR))
			pause()
			return
		self.show_cart()
		print(color("Ketik 'b' atau 'B' untuk membatalkan dan kembali ke menu utama.", COLOR_INPUT))
		pid_input: str = input("Masukkan ID produk untuk dihapus: ").strip()
		if pid_input.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		try:
			pid = int(pid_input)
		except ValueError:
			print(color("Masukan tidak valid. Masukkan bilangan bulat.", COLOR_ERROR))
			pause()
			return
		idx: int | None = next((i for i, c in enumerate(self.cart) if c['id'] == pid), None)
		if idx is None:
			print(color("Item tidak ditemukan di keranjang.", COLOR_ERROR))
			pause()
			return
		removed = self.cart.pop(idx)
		print(color(f"Berhasil menghapus {removed['name']} dari keranjang.", COLOR_OK))
		pause()

	def show_cart(self) -> None:
		"""Menampilkan isi keranjang belanja yang sedang aktif."""
		print(color("ID  Nama                 Qty  Harga (IDR)   Subtotal (IDR)", COLOR_MENU))
		print(color("--  -------------------- --- -----------   ---------------", COLOR_MENU))
		total = 0
		for c in self.cart:
			subtotal = c['qty'] * c['price']
			total += subtotal
			print(f"{c['id']:2}  {c['name'][:20]:20} {c['qty']:3} {format_idr(c['price']):>13}  {format_idr(subtotal):>14}")
		print(f"\nTotal: {format_idr(total)}")

	# =========================================================
	# Logika Transaksi (Transaction Logic)
	# ---------------------------------------------------------
	# Bagian ini menangani proses transaksi, mulai dari checkout,
	# menerima pembayaran, menghitung kembalian, dan mengosongkan
	# keranjang setelah transaksi selesai.
	# =========================================================
	def checkout(self) -> None:
		"""Menangani proses checkout: pembayaran, kembalian, dan pembuatan struk."""
		clear_screen()
		print(color("=== Checkout ===", COLOR_HEADER))
		if not self.cart:
			print(color("Keranjang kosong.", COLOR_ERROR))
			pause()
			return
		
		# Customer Name Input
		print(color("\n--- Informasi Pelanggan ---", COLOR_MENU))
		customer_name: str = input("Nama pelanggan: ").strip()
		if customer_name.lower() == 'b':
			print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
			pause()
			return
		if not customer_name:
			customer_name = "Guest"
		
		self.show_cart()
		print(color("Ketik 'b' atau 'B' untuk membatalkan dan kembali ke menu utama.", COLOR_INPUT))
		total: int = sum(c['qty'] * c['price'] for c in self.cart)
		
		# Payment Method Selection
		print(color("\n--- Metode Pembayaran ---", COLOR_MENU))
		print(color("1. Tunai", COLOR_MENU))
		print(color("2. QRIS", COLOR_MENU))
		while True:
			payment_method_input: str = input("Pilih metode pembayaran (1 atau 2): ").strip()
			if payment_method_input.lower() == 'b':
				print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
				pause()
				return
			if payment_method_input in ['1', '2']:
				break
			print(color("Pilihan tidak valid. Masukkan 1 atau 2.", COLOR_ERROR))
		
		payment_method = "Tunai" if payment_method_input == '1' else "QRIS"
		
		# Handle different payment methods
		if payment_method == "Tunai":
			while True:
				cash_input: str = input(f"Uang yang diterima (total {format_idr(total)}): ")
				if cash_input.lower() == 'b':
					print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
					pause()
					return
				try:
					cash = float(cash_input)
					if cash < total:
						print(color("Uang tidak cukup. Masukkan jumlah yang tepat.", COLOR_ERROR))
						continue
					break
				except ValueError:
					print(color("Masukan tidak valid. Masukkan angka.", COLOR_ERROR))
					continue
			change: float = cash - total
			print(color(f"Kembalian: {format_idr(change)}", COLOR_OK))
			self.generate_receipt(total, cash, change, customer_name, payment_method)
		else:  # QRIS
			print(color("\n--- Pembayaran QRIS ---", COLOR_MENU))
			self.display_qr_code(total)
			input(color("Tekan Enter setelah pembayaran berhasil: ", COLOR_INPUT))
			self.generate_receipt(total, total, 0, customer_name, payment_method)
		
		print(color("Struk berhasil dibuat.", COLOR_OK))
		self.cart.clear()
		pause()

	# ---------------------------------------------------------
	# Penanganan Struk (Receipt Handling)
	# ---------------------------------------------------------
	# Bagian ini membuat dan menyimpan struk transaksi dalam
	# bentuk file teks, berisi detail pembelian, total, pembayaran,
	# dan kembalian.
	def generate_receipt(self, total, cash, change, customer_name: str = "Guest", payment_method: str = "Cash") -> None:
		"""Membuat dan menyimpan struk transaksi ke file teks."""
		timestamp = get_timestamp()
		filename = f"struk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
		with open(filename, 'w', encoding='utf-8') as f:
			f.write("STRUK PEMBELIAN - SCHOOL POS\n")
			f.write(f"Tanggal: {timestamp}\n")
			f.write(f"Pelanggan: {customer_name}\n")
			f.write(f"Metode Pembayaran: {payment_method}\n\n")
			f.write("Barang Belanja:\n")
			f.write("ID  Nama                 Qty  Harga (IDR)   Subtotal (IDR)\n")
			f.write("--  -------------------- --- -----------   ---------------\n")
			for c in self.cart:
				subtotal = c['qty'] * c['price']
				f.write(f"{c['id']:2}  {c['name'][:20]:20} {c['qty']:3} {format_idr(c['price']):>13}  {format_idr(subtotal):>14}\n")
			f.write(f"\nTotal Harga:   {format_idr(total)}\n")
			if payment_method == "Tunai":
				f.write(f"Uang Masuk:    {format_idr(cash)}\n")
				f.write(f"Kembalian:     {format_idr(change)}\n")
			else:
				f.write(f"Dibayar melalui {payment_method}\n")
		print(color(f"Struk berhasil disimpan sebagai {filename}", COLOR_OK))

	def display_qr_code(self, amount: float) -> None:
		"""Menampilkan kode QR di terminal untuk pembayaran QRIS."""
		try:
			# URL untuk pembayaran
			payment_url = f"https://aspectxlol.vercel.app/uprak-pos/payment?amount={int(amount)}"
			
			# Generate QR code
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=2,
				border=2,
			)
			qr.add_data(payment_url)
			qr.make(fit=True)
			
			# Get QR code sebagai ASCII art
			ascii_qr = qr.get_matrix()
			
			print(color("\n╔══════════════════════════════════════════════════╗", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("║       PEMBAYARAN QRIS - PINDAI DENGAN PONSEL      ║", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("╚══════════════════════════════════════════════════╝", COLOR_OK))
			print()
			
			# Display QR code
			for row in ascii_qr:
				line = "  "
				for cell in row:
					line += "██" if cell else "  "
				print(color(line, COLOR_OK))
			
			print()
			print(color("╔══════════════════════════════════════════════════╗", COLOR_OK))
			print(color("║  Nominal: " + format_idr(amount)[:38].ljust(38) + " ║", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("╚══════════════════════════════════════════════════╝", COLOR_OK))
			
		except Exception as e:
			print(color(f"Kesalahan saat membuat kode QR: {e}", COLOR_ERROR))
			# Fallback: just show the payment URL
			payment_url = f"https://aspectxlol.vercel.app/uprak-pos/payment?amount={int(amount)}"
			
			print(color("\n╔══════════════════════════════════════════════════╗", COLOR_OK))
			print(color("║       PEMBAYARAN QRIS                             ║", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("║  Nominal: " + format_idr(amount)[:38].ljust(38) + " ║", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("║  Buka tautan ini di ponsel Anda:                 ║", COLOR_OK))
			print(color("║  " + payment_url[:44] + " ║", COLOR_OK))
			print(color("║                                                  ║", COLOR_OK))
			print(color("╚══════════════════════════════════════════════════╝", COLOR_OK))
	

# =========================================================
# Tampilan Menu (Menu Rendering)
# ---------------------------------------------------------
# Bagian ini menampilkan menu utama dan menerima pilihan
# pengguna untuk menjalankan fitur-fitur POS.
# =========================================================
def main_menu() -> str:
	"""Menampilkan menu utama dan mengembalikan pilihan pengguna."""
	clear_screen()
	print(color("=== SISTEM POS SEKOLAH ===", COLOR_HEADER))
	print(color("1. Tambah Produk", COLOR_MENU))
	print(color("2. Edit Produk", COLOR_MENU))
	print(color("3. Lihat Daftar Produk", COLOR_MENU))
	print(color("4. Tambah ke Keranjang", COLOR_MENU))
	print(color("5. Hapus dari Keranjang", COLOR_MENU))
	print(color("6. Lihat Keranjang", COLOR_MENU))
	print(color("7. Checkout", COLOR_MENU))
	print(color("0. Keluar", COLOR_MENU))
	return input(color("Pilih opsi: ", COLOR_INPUT)).strip()

# =========================================================
# Loop Utama (Main Loop)
# ---------------------------------------------------------
# Bagian utama yang menjalankan aplikasi POS secara terus-
# menerus sampai pengguna memilih keluar. Semua interaksi
# pengguna terjadi di sini.
# =========================================================
def main() -> None:
	"""Perulangan utama aplikasi POS."""
	pos = POS()
	while True:
		choice: str = main_menu()
		if choice == '1':
			pos.add_product()
		elif choice == '2':
			pos.edit_product()
		elif choice == '3':
			clear_screen()
			print(color("=== Daftar Produk ===", COLOR_HEADER))
			if not pos.products:
				print(color("Tidak ada produk yang tersedia.", COLOR_ERROR))
			else:
				pos.list_products()
			pause()
		elif choice == '4':
			pos.add_to_cart()
		elif choice == '5':
			pos.remove_from_cart()
		elif choice == '6':
			clear_screen()
			print(color("=== Keranjang ===", COLOR_HEADER))
			if not pos.cart:
				print(color("Keranjang kosong.", COLOR_ERROR))
			else:
				pos.show_cart()
			pause()
		elif choice == '7':
			pos.checkout()
		elif choice == '0':
			print(color("Keluar dari POS. Sampai jumpa!", COLOR_HEADER))
			break
		else:
			print(color("Pilihan tidak valid.", COLOR_ERROR))
			pause()

if __name__ == "__main__":
	main()
