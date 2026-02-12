import os
import csv
import sys
import json
import base64
import time
from datetime import datetime
import qrcode

# =========================================================
# Color Constants
# =========================================================
COLOR_HEADER = '96'   # Bright cyan
COLOR_MENU = '93'     # Bright yellow
COLOR_OK = '92'       # Bright green
COLOR_ERROR = '91'    # Bright red
COLOR_INPUT = '94'    # Bright blue
COLOR_RESET = '0'

def color(text: str, code: str) -> str:
    """Pembungkus untuk kode warna ANSI di terminal."""
    return f"\033[{code}m{text}\033[0m"

def clear_screen() -> None:
    """Membersihkan layar terminal untuk tampilan yang lebih rapi."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg: str = "Tekan Enter untuk melanjutkan...") -> None:
    """Menghentikan eksekusi sampai pengguna menekan Enter."""
    input(msg)

def input_text(prompt: str) -> str:
    """Meminta input teks."""
    return input(prompt)

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

    def _validate_price(self, price_str: str) -> bool:
        """Validasi input harga."""
        try:
            price = float(price_str)
            return price > 0
        except ValueError:
            return False

    def save_products(self) -> None:
        """Menyimpan semua produk ke file CSV."""
        with open(self.products_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'price'])
            writer.writeheader()
            for p in self.products:
                writer.writerow({'id': p['id'], 'name': p['name'], 'price': p['price']})

    def list_products(self, show_header=True) -> None:
        """Menampilkan semua produk yang tersedia."""
        if show_header:
            print(color("ID  Nama                 Harga (IDR)", COLOR_MENU))
            print(color("--  -------------------- -----------", COLOR_MENU))
        for p in self.products:
            print(f"{p['id']:2}  {p['name'][:20]:20} {format_idr(p['price']):>13}")

    def add_product(self) -> None:
        """Menambahkan produk baru ke daftar dan menyimpan ke file."""
        clear_screen()
        print(color("=== Tambah Produk ===", COLOR_HEADER))
        
        try:
            name = input_text("Nama produk: ").strip()
            if not name:
                print(color("Nama tidak boleh kosong.", COLOR_ERROR))
                pause()
                return
            
            price_str = input_text("Harga produk: ").strip()
            if not self._validate_price(price_str):
                print(color("Harga tidak valid. Masukkan angka positif.", COLOR_ERROR))
                pause()
                return
            
            price = float(price_str)
            
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
        except KeyboardInterrupt:
            print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
            pause()

    def edit_product(self) -> None:
        """Mengedit produk yang ada dengan ID dan menyimpan ke file."""
        clear_screen()
        print(color("=== Edit Produk ===", COLOR_HEADER))
        if not self.products:
            print(color("Tidak ada produk untuk diedit.", COLOR_ERROR))
            pause()
            return
        
        try:
            self.list_products()
            pid_input = input_text("Masukkan ID produk untuk diedit: ").strip()
            if not pid_input.isdigit():
                print(color("ID harus berupa angka.", COLOR_ERROR))
                pause()
                return
            
            pid = int(pid_input)
            product = next((p for p in self.products if p['id'] == pid), None)
            
            if not product:
                print(color("Produk tidak ditemukan.", COLOR_ERROR))
                pause()
                return
            
            print(f"Mengedit '{product['name']}'")
            new_name = input_text(f"Nama baru (kosongkan untuk tetap '{product['name']}'): ").strip()
            if new_name:
                product['name'] = new_name
            
            new_price = input_text(f"Harga baru (kosongkan untuk tetap {format_idr(product['price'])}): ").strip()
            if new_price:
                if self._validate_price(new_price):
                    product['price'] = float(new_price)
                else:
                    print(color("Harga tidak valid.", COLOR_ERROR))
            
            self.save_products()
            print(color("Produk berhasil diperbarui.", COLOR_OK))
            pause()
        except KeyboardInterrupt:
            print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
            pause()

    def add_to_cart(self) -> None:
        """Menambahkan produk ke keranjang berdasarkan ID dan jumlah."""
        clear_screen()
        print(color("=== Tambah ke Keranjang ===", COLOR_HEADER))
        if not self.products:
            print(color("Tidak ada produk yang tersedia.", COLOR_ERROR))
            pause()
            return
        
        try:
            self.list_products()
            pid_input = input_text("Masukkan ID produk untuk ditambahkan: ").strip()
            if not pid_input.isdigit():
                print(color("ID harus berupa angka.", COLOR_ERROR))
                pause()
                return
            
            pid = int(pid_input)
            product = next((p for p in self.products if p['id'] == pid), None)
            
            if not product:
                print(color("Produk tidak ditemukan.", COLOR_ERROR))
                pause()
                return
            
            qty_input = input_text("Jumlah: ").strip()
            if not qty_input.isdigit() or int(qty_input) <= 0:
                print(color("Jumlah tidak valid.", COLOR_ERROR))
                pause()
                return
            
            qty = int(qty_input)
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
        except KeyboardInterrupt:
            print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
            pause()

    def remove_from_cart(self) -> None:
        """Menghapus item dari keranjang berdasarkan ID produk."""
        clear_screen()
        print(color("=== Hapus dari Keranjang ===", COLOR_HEADER))
        if not self.cart:
            print(color("Keranjang kosong.", COLOR_ERROR))
            pause()
            return
        
        try:
            self.show_cart()
            pid_input = input_text("Masukkan ID produk untuk dihapus: ").strip()
            if not pid_input.isdigit():
                print(color("ID harus berupa angka.", COLOR_ERROR))
                pause()
                return
            
            pid = int(pid_input)
            idx = next((i for i, c in enumerate(self.cart) if c['id'] == pid), None)
            
            if idx is None:
                print(color("Item tidak ditemukan di keranjang.", COLOR_ERROR))
                pause()
                return
            
            removed = self.cart.pop(idx)
            print(color(f"Berhasil menghapus {removed['name']} dari keranjang.", COLOR_OK))
            pause()
        except KeyboardInterrupt:
            print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
            pause()

    def show_cart(self) -> None:
        """Menampilkan isi keranjang belanja yang sedang aktif."""
        if not self.cart:
            print(color("Keranjang kosong.", COLOR_ERROR))
            return
        print(color("ID  Nama                 Qty  Harga (IDR)   Subtotal (IDR)", COLOR_MENU))
        print(color("--  -------------------- --- -----------   ---------------", COLOR_MENU))
        total = 0
        for c in self.cart:
            subtotal = c['qty'] * c['price']
            total += subtotal
            print(f"{c['id']:2}  {c['name'][:20]:20} {c['qty']:3} {format_idr(c['price']):>13}  {format_idr(subtotal):>14}")
        print(f"\nTotal: {format_idr(total)}")

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

    def display_qr_code(self, amount: float, customer_name: str = "Guest") -> None:
        """Menampilkan kode QR di terminal untuk pembayaran QRIS."""
        try:
            payment_data = {
                "merchantName": "Ujian Praktek",
                "customerName": customer_name,
                "price": str(int(amount))
            }
            encoded_data = base64.b64encode(json.dumps(payment_data).encode()).decode()
            payment_url = f"https://aspectxlol.vercel.app/uprak-pos/payment?data={encoded_data}"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=1,
                border=1,
            )
            qr.add_data(payment_url)
            qr.make(fit=True)
            ascii_qr = qr.get_matrix()
            
            print(color("\n╔════════════════════════════════════╗", COLOR_OK))
            print(color("║    PEMBAYARAN QRIS - PINDAI PONSEL  ║", COLOR_OK))
            print(color("╚════════════════════════════════════╝", COLOR_OK))
            print()
            
            for row in ascii_qr:
                line = ""
                for cell in row:
                    line += "██" if cell else "  "
                print(color(line, COLOR_OK))
            
            print()
            print(color("╔════════════════════════════════════╗", COLOR_OK))
            print(color(f"║ Nominal: {format_idr(amount)[:24].ljust(24)} ║", COLOR_OK))
            print(color("╚════════════════════════════════════╝", COLOR_OK))
        except Exception as e:
            print(color(f"Kesalahan saat membuat kode QR: {e}", COLOR_ERROR))

    def checkout(self) -> None:
        """Menangani proses checkout: pembayaran, kembalian, dan pembuatan struk."""
        clear_screen()
        print(color("=== Checkout ===", COLOR_HEADER))
        if not self.cart:
            print(color("Keranjang kosong.", COLOR_ERROR))
            pause()
            return
        
        try:
            customer_name = input_text("Nama pelanggan (atau tekan Enter untuk 'Guest'): ").strip() or "Guest"
            
            self.show_cart()
            total = sum(c['qty'] * c['price'] for c in self.cart)
            
            print(color("\n--- Metode Pembayaran ---", COLOR_MENU))
            print("1. Tunai")
            print("2. QRIS")
            
            while True:
                method_input = input_text("Pilih metode (1 atau 2): ").strip()
                if method_input in ['1', '2']:
                    break
                print(color("Pilihan tidak valid.", COLOR_ERROR))
            
            payment_method = "Tunai" if method_input == '1' else "QRIS"
            
            if payment_method == "Tunai":
                while True:
                    cash_input = input_text(f"Uang yang diterima (total {format_idr(total)}): ").strip()
                    try:
                        cash = float(cash_input)
                        if cash >= total:
                            break
                        print(color("Uang tidak cukup.", COLOR_ERROR))
                    except ValueError:
                        print(color("Input tidak valid.", COLOR_ERROR))
                
                change = cash - total
                print(color(f"Kembalian: {format_idr(change)}", COLOR_OK))
                self.generate_receipt(total, cash, change, customer_name, payment_method)
            else:
                print(color("\nPembayaran QRIS", COLOR_MENU))
                self.display_qr_code(total, customer_name)
                input_text("Tekan Enter setelah pembayaran berhasil...")
                self.generate_receipt(total, total, 0, customer_name, payment_method)
            
            print(color("Struk berhasil dibuat.", COLOR_OK))
            self.cart.clear()
            pause()
        except KeyboardInterrupt:
            print(color("Dibatalkan. Kembali ke menu utama.", COLOR_ERROR))
            pause()

def main_menu() -> str:
    """Menampilkan menu utama dengan TUI berdasarkan text input."""
    clear_screen()
    
    width = 80
    print(color("╔" + "═" * (width - 2) + "╗", COLOR_HEADER))
    header = "═══ SISTEM POS SEKOLAH ═══"
    header_x = (width - len(header) - 2) // 2
    print(color("║" + " " * header_x + header + " " * (width - header_x - len(header) - 2) + "║", COLOR_HEADER))
    print(color("╠" + "═" * (width - 2) + "╣", COLOR_HEADER))
    
    menu_items = [
        "1. Tambah Produk",
        "2. Edit Produk",
        "3. Lihat Daftar Produk",
        "4. Tambah ke Keranjang",
        "5. Hapus dari Keranjang",
        "6. Lihat Keranjang",
        "7. Checkout",
        "0. Keluar"
    ]
    
    for item in menu_items:
        print(color("║ " + item.ljust(width - 4) + " ║", COLOR_HEADER))
    
    print(color("╠" + "═" * (width - 2) + "╣", COLOR_HEADER))
    print(color("║ Masukkan angka pilihan (0-7)" + " " * (width - 32) + "║", COLOR_INPUT))
    print(color("╚" + "═" * (width - 2) + "╝", COLOR_HEADER))
    
    try:
        choice = input_text("\nPilihan: ").strip()
        return choice if choice in ['0', '1', '2', '3', '4', '5', '6', '7'] else 'x'
    except KeyboardInterrupt:
        return '0'

def run_application() -> None:
    """Perulangan utama aplikasi POS."""
    pos = POS()
    while True:
        choice = main_menu()
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
            pos.show_cart()
            pause()
        elif choice == '7':
            pos.checkout()
        elif choice == '0':
            clear_screen()
            print(color("Keluar dari POS. Sampai jumpa!", COLOR_HEADER))
            break
        else:
            print(color("Pilihan tidak valid. Masukkan angka 0-7.", COLOR_ERROR))
            pause()

if __name__ == "__main__":
    run_application()
