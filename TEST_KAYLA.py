import qrcode

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

def format_idr(amount: float) -> str:
	"""Memformat angka menjadi Rupiah Indonesia (IDR)."""
	return f"Rp {int(amount):,}".replace(",", ".")

def display_qr_code(amount: float) -> None:
    """Menampilkan kode QR di terminal untuk pembayaran QRIS."""
    try:
        # URL untuk pembayaran
        payment_url = f"https://aspectxlol.vercel.app/uprak-pos/payment?amount={int(amount)}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
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
            line = ""
            for cell in row:
                line += "█" if cell else " "
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

display_qr_code(12000)