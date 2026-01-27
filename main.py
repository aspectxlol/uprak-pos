
# =========================================================
# Impor Modul (Imports)
# ---------------------------------------------------------
# Bagian ini mengimpor modul-modul Python yang diperlukan
# untuk menjalankan aplikasi POS, seperti modul file, CSV,
# dan waktu.
# =========================================================
import os
import csv
from datetime import datetime

# =========================================================
# Utilitas Warna Terminal (Color Utility)
# ---------------------------------------------------------
# Bagian ini berisi fungsi dan variabel untuk memberikan
# warna pada teks di terminal, sehingga tampilan lebih
# mudah dibaca dan menarik.
# =========================================================
def color(text: str, code: str) -> str:
    """Wraps text in ANSI color codes if supported."""
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
    """Clears the terminal screen for better UI readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg: str = "Press Enter to continue...") -> None:
    """Pauses execution until user presses Enter."""
    input(color(msg, COLOR_INPUT))

def input_number(prompt: str, allow_zero: bool = False) -> float:
    """Prompts user for a number, keeps asking until valid."""
    while True:
        val = input(prompt)
        try:
            num = float(val)
            if not allow_zero and num <= 0:
                print("Please enter a positive number.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a number.")

def input_int(prompt: str, allow_zero: bool = False) -> int:
    """Prompts user for an integer, keeps asking until valid."""
    while True:
        val = input(prompt)
        try:
            num = int(val)
            if not allow_zero and num <= 0:
                print("Please enter a positive integer.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_timestamp() -> str:
    """Returns current date and time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_idr(amount: float) -> str:
    """Formats a number as Indonesian Rupiah (IDR)."""
    return f"Rp {int(amount):,}".replace(",", ".")

# =========================================================
# Model Data / Kelas Utama (Data Models / Main Class)
# ---------------------------------------------------------
# Bagian utama aplikasi POS. Kelas POS menyimpan data produk,
# keranjang belanja, dan mengelola seluruh logika utama
# seperti menambah produk, transaksi, dan pembuatan struk.
# =========================================================
class POS:
	"""Main POS class to manage products, cart, and transactions."""
	def __init__(self) -> None:
		self.products = []  # List of dicts: {id, name, price}
		self.cart = []      # List of dicts: {id, name, price, qty}
		self.next_product_id = 1
		self.products_file = "products.csv"
		self.load_products()

	def load_products(self) -> None:
		"""Loads products from a CSV file if it exists."""
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
		"""Saves products to a CSV file."""
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
	"""Adds a new product to the product list and saves to file."""
	clear_screen()
	print(color("=== Add Product ===", COLOR_HEADER))
	print(color("Type 'b' or 'B' at any prompt to cancel and return to main menu.", COLOR_INPUT))
	name: str = input("Product name: ").strip()
	if name.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	price_input: str = input("Product price: ")
	if price_input.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	try:
		price = float(price_input)
		if price <= 0:
			print(color("Please enter a positive number.", COLOR_ERROR))
			pause()
			return
	except ValueError:
		print(color("Invalid input. Please enter a number.", COLOR_ERROR))
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
	print(color(f"Product '{name}' added with ID {product['id']}", COLOR_OK))
	pause()

def edit_product(self) -> None:
	"""Edits an existing product by ID and saves to file."""
	clear_screen()
	print(color("=== Edit Product ===", COLOR_HEADER))
	if not self.products:
		print(color("No products to edit.", COLOR_ERROR))
		pause()
		return
	self.list_products()
	print(color("Type 'b' or 'B' at any prompt to cancel and return to main menu.", COLOR_INPUT))
	pid_input: str = input("Enter product ID to edit: ").strip()
	if pid_input.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	try:
		pid = int(pid_input)
	except ValueError:
		print(color("Invalid input. Please enter an integer.", COLOR_ERROR))
		pause()
		return
	product = next((p for p in self.products if p['id'] == pid), None)
	if not product:
		print(color("Product not found.", COLOR_ERROR))
		pause()
		return
	print(f"Editing '{product['name']}' (ID {product['id']})")
	new_name: str = input(f"New name (leave blank to keep '{product['name']}'): ").strip()
	if new_name.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	if new_name:
		product['name'] = new_name
	new_price: str = input(f"New price (leave blank to keep {product['price']}): ").strip()
	if new_price.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	if new_price:
		try:
			product['price'] = float(new_price)
		except ValueError:
			print(color("Invalid price. Keeping old price.", COLOR_ERROR))
	self.save_products()
	print(color("Product updated.", COLOR_OK))
	pause()

def list_products(self, show_header=True) -> None:
	"""Displays all products."""
	if show_header:
		print(color("ID  Name                 Price (IDR)", COLOR_MENU))
		print(color("--  -------------------- -------------", COLOR_MENU))
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
	"""Adds a product to the cart by ID and quantity."""
	clear_screen()
	print(color("=== Add to Cart ===", COLOR_HEADER))
	if not self.products:
		print(color("No products available.", COLOR_ERROR))
		pause()
		return
	self.list_products()
	print(color("Type 'b' or 'B' at any prompt to cancel and return to main menu.", COLOR_INPUT))
	pid_input: str = input("Enter product ID to add: ").strip()
	if pid_input.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	try:
		pid = int(pid_input)
	except ValueError:
		print(color("Invalid input. Please enter an integer.", COLOR_ERROR))
		pause()
		return
	product = next((p for p in self.products if p['id'] == pid), None)
	if not product:
		print(color("Product not found.", COLOR_ERROR))
		pause()
		return
	qty_input: str = input("Quantity: ").strip()
	if qty_input.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	try:
		qty = int(qty_input)
		if qty <= 0:
			print(color("Please enter a positive integer.", COLOR_ERROR))
			pause()
			return
	except ValueError:
		print(color("Invalid input. Please enter an integer.", COLOR_ERROR))
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
	print(color(f"Added {qty} x {product['name']} to cart.", COLOR_OK))
	pause()

def remove_from_cart(self) -> None:
	"""Removes an item from the cart by product ID."""
	clear_screen()
	print(color("=== Remove from Cart ===", COLOR_HEADER))
	if not self.cart:
		print(color("Cart is empty.", COLOR_ERROR))
		pause()
		return
	self.show_cart()
	print(color("Type 'b' or 'B' at any prompt to cancel and return to main menu.", COLOR_INPUT))
	pid_input: str = input("Enter product ID to remove: ").strip()
	if pid_input.lower() == 'b':
		print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
		pause()
		return
	try:
		pid = int(pid_input)
	except ValueError:
		print(color("Invalid input. Please enter an integer.", COLOR_ERROR))
		pause()
		return
	idx: int | None = next((i for i, c in enumerate(self.cart) if c['id'] == pid), None)
	if idx is None:
		print(color("Item not found in cart.", COLOR_ERROR))
		pause()
		return
	removed = self.cart.pop(idx)
	print(color(f"Removed {removed['name']} from cart.", COLOR_OK))
	pause()

def show_cart(self) -> None:
	"""Displays the current cart contents."""
	print(color("ID  Name                 Qty  Price (IDR)   Subtotal (IDR)", COLOR_MENU))
	print(color("--  -------------------- --- -------------  --------------", COLOR_MENU))
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
	"""Handles the checkout process: payment, change, and receipt."""
	clear_screen()
	print(color("=== Checkout ===", COLOR_HEADER))
	if not self.cart:
		print(color("Cart is empty.", COLOR_ERROR))
		pause()
		return
	self.show_cart()
	print(color("Type 'b' or 'B' at any prompt to cancel and return to main menu.", COLOR_INPUT))
	total: int = sum(c['qty'] * c['price'] for c in self.cart)
	while True:
		cash_input: str = input(f"Cash received (total {format_idr(total)}): ")
		if cash_input.lower() == 'b':
			print(color("Cancelled. Returning to main menu...", COLOR_ERROR))
			pause()
			return
		try:
			cash = float(cash_input)
			if cash < total:
				print(color("Not enough cash. Please enter a valid amount.", COLOR_ERROR))
				continue
			break
		except ValueError:
			print(color("Invalid input. Please enter a number.", COLOR_ERROR))
			continue
	change: float = cash - total
	print(color(f"Change: {format_idr(change)}", COLOR_OK))
	self.generate_receipt(total, cash, change)
	print(color("Receipt generated.", COLOR_OK))
	self.cart.clear()
	pause()

# ---------------------------------------------------------
# Penanganan Struk (Receipt Handling)
# ---------------------------------------------------------
# Bagian ini membuat dan menyimpan struk transaksi dalam
# bentuk file teks, berisi detail pembelian, total, pembayaran,
# dan kembalian.
def generate_receipt(self, total, cash, change) -> None:
	"""Generates and saves a receipt as a .txt file."""
	timestamp = get_timestamp()
	filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
	with open(filename, 'w', encoding='utf-8') as f:
		f.write("SCHOOL POS RECEIPT\n")
		f.write(f"Date: {timestamp}\n\n")
		f.write("Items:\n")
		f.write("ID  Name                 Qty  Price (IDR)   Subtotal (IDR)\n")
		f.write("--  -------------------- --- -------------  --------------\n")
		for c in self.cart:
			subtotal = c['qty'] * c['price']
			f.write(f"{c['id']:2}  {c['name'][:20]:20} {c['qty']:3} {format_idr(c['price']):>13}  {format_idr(subtotal):>14}\n")
		f.write(f"\nTotal:   {format_idr(total)}\n")
		f.write(f"Cash:    {format_idr(cash)}\n")
		f.write(f"Change:  {format_idr(change)}\n")
	print(color(f"Receipt saved as {filename}", COLOR_OK))

# =========================================================
# Tampilan Menu (Menu Rendering)
# ---------------------------------------------------------
# Bagian ini menampilkan menu utama dan menerima pilihan
# pengguna untuk menjalankan fitur-fitur POS.
# =========================================================
def main_menu() -> str:
	"""Displays the main menu and returns the user's choice."""
	clear_screen()
	print(color("=== SCHOOL POS SYSTEM ===", COLOR_HEADER))
	print(color("1. Add Product", COLOR_MENU))
	print(color("2. Edit Product", COLOR_MENU))
	print(color("3. List Products", COLOR_MENU))
	print(color("4. Add to Cart", COLOR_MENU))
	print(color("5. Remove from Cart", COLOR_MENU))
	print(color("6. Show Cart", COLOR_MENU))
	print(color("7. Checkout", COLOR_MENU))
	print(color("0. Exit", COLOR_MENU))
	return input(color("Select an option: ", COLOR_INPUT)).strip()

# =========================================================
# Loop Utama (Main Loop)
# ---------------------------------------------------------
# Bagian utama yang menjalankan aplikasi POS secara terus-
# menerus sampai pengguna memilih keluar. Semua interaksi
# pengguna terjadi di sini.
# =========================================================
def main() -> None:
	"""Main application loop."""
	pos = POS()
	while True:
		choice: str = main_menu()
		if choice == '1':
			pos.add_product()
		elif choice == '2':
			pos.edit_product()
		elif choice == '3':
			clear_screen()
			print(color("=== Product List ===", COLOR_HEADER))
			if not pos.products:
				print(color("No products available.", COLOR_ERROR))
			else:
				pos.list_products()
			pause()
		elif choice == '4':
			pos.add_to_cart()
		elif choice == '5':
			pos.remove_from_cart()
		elif choice == '6':
			clear_screen()
			print(color("=== Cart ===", COLOR_HEADER))
			if not pos.cart:
				print(color("Cart is empty.", COLOR_ERROR))
			else:
				pos.show_cart()
			pause()
		elif choice == '7':
			pos.checkout()
		elif choice == '0':
			print(color("Exiting POS. Goodbye!", COLOR_HEADER))
			break
		else:
			print(color("Invalid option.", COLOR_ERROR))
			pause()

if __name__ == "__main__":
	main()