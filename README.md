# 🛒 UPRAK-POS

> A lightweight, terminal-based Point of Sale system built in Python — designed for small businesses, school canteens, and educational demonstration.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Google%20Colab%20%7C%20Terminal-orange)
![Storage](https://img.shields.io/badge/Storage-CSV%20%2B%20TXT-green)
![Payment](https://img.shields.io/badge/Payment-Cash%20%2B%20QRIS-purple)
![License](https://img.shields.io/badge/License-Open%20Source-lightgrey)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Data Structures](#data-structures)
- [Installation](#installation)
- [Usage](#usage)
- [Code Architecture](#code-architecture)
- [Dependencies](#dependencies)
- [Customization](#customization)
- [Limitations](#limitations)
- [License](#license)

---

## Overview

UPRAK-POS is a command-line Point of Sale system that handles product management, cart operations, and sales transactions — all without a database. Data is persisted in a plain `products.csv` file, and a timestamped receipt `.txt` is generated after every checkout.

Built as an **UPRAK (Ujian Praktik)** project, it demonstrates core Python concepts including:
- Object-Oriented Programming (OOP)
- File I/O with CSV
- List and dictionary data structures
- Input validation and error handling
- Terminal UI with ANSI color codes

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Product Management** | Add products with name and price. Edit existing products by ID. View full catalog as a formatted table. |
| 2 | **Shopping Cart** | Add products to cart by ID and quantity. Accumulates qty if product already exists. |
| 3 | **Remove from Cart** | Remove individual items from the active cart before checkout. |
| 4 | **Checkout** | Review cart, accept Cash or QRIS payment, calculate change automatically. |
| 5 | **Receipt Generation** | Auto-saves a timestamped `struk_YYYYMMDD_HHMMSS.txt` after every transaction. |
| 6 | **QRIS Payment** | Generates a scannable QR code using the `qrcode` library with encoded payment data. |
| 7 | **Color-coded UI** | ANSI escape codes: cyan headers, yellow menus, green for success, red for errors. |
| 8 | **Input Validation** | All inputs validated — numeric checks, empty string checks, ID existence checks. |

---

## File Structure

```
UPRAK-POS/
├── main.py                        # Main application script
├── UPRAK_POS_System.ipynb         # Google Colab notebook version
├── products.csv                   # Product catalog (auto-created on first run)
├── struk_20240101_120000.txt      # Example generated receipt
└── README.md                      # This file
```

### File Descriptions

| File | Description |
|------|-------------|
| `main.py` | Core application. Contains the `POS` class and all methods. Entry point for local use. |
| `*.ipynb` | Colab-compatible notebook. Each cell is a module — run top to bottom. |
| `products.csv` | Stores product catalog. Auto-created if missing. Can be manually edited. |
| `struk_*.txt` | Generated after each checkout. Contains items, totals, payment method, and change. |

---

## Data Structures

UPRAK-POS uses two core data structures throughout the application:

### `products` — List of Dictionaries
Loaded from `products.csv` at startup. Each entry has three keys:

```python
products = [
    {"id": 1, "name": "Nasi Goreng", "price": 12000},
    {"id": 2, "name": "Teh Manis",   "price": 5000},
    {"id": 3, "name": "Es Jeruk",    "price": 7000},
]
```

### `cart` — List of Dictionaries
Built during an active session. Adds a `qty` field on top of product data. Cleared after successful checkout.

```python
cart = [
    {"id": 1, "name": "Nasi Goreng", "price": 12000, "qty": 2},
    {"id": 2, "name": "Teh Manis",   "price": 5000,  "qty": 1},
]
```

### `products.csv` Format

```
id,name,price
1,Nasi Goreng,12000
2,Teh Manis,5000
3,Es Jeruk,7000
```

---

## Installation

### Option A — Google Colab *(Recommended)*

1. Open [Google Colab](https://colab.research.google.com) and upload `UPRAK_POS_System.ipynb`
2. Run the first cell to install dependencies:
   ```
   %pip install qrcode[pil]
   ```
3. Run all cells from top to bottom
4. Run the final cell to launch:
   ```python
   run_application()
   ```

### Option B — Local Python Environment

1. Make sure Python 3 is installed
2. Install the required library:
   ```bash
   pip install qrcode[pil]
   ```
3. Run the application:
   ```bash
   python main.py
   ```

> **Note:** Color-coded output requires a terminal that supports ANSI escape codes (Linux, macOS, Windows Terminal, VS Code). Standard `cmd.exe` on Windows may not display colors correctly.

---

## Usage

### Main Menu

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      ═══ SISTEM POS SEKOLAH ═══                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  1. Tambah Produk                                                          ║
║  2. Edit Produk                                                            ║
║  3. Lihat Daftar Produk                                                    ║
║  4. Tambah ke Keranjang                                                    ║
║  5. Hapus dari Keranjang                                                   ║
║  6. Lihat Keranjang                                                        ║
║  7. Checkout                                                               ║
║  0. Keluar                                                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Making a Sale — Step by Step

1. Press `1` to add products if none exist yet
2. Press `4` to add a product to cart — enter product ID, then quantity
3. Repeat for all items the customer wants
4. Press `6` to review the cart and verify totals
5. Press `7` to checkout:
   - Enter customer name (or press Enter for `Guest`)
   - Choose payment: `1` for Cash, `2` for QRIS
   - **Cash:** enter amount received — change is calculated automatically
   - **QRIS:** scan the QR code displayed on screen, then press Enter to confirm
6. Receipt is saved automatically as `struk_YYYYMMDD_HHMMSS.txt`

### Sample Receipt

```
STRUK PEMBELIAN - SCHOOL POS
Tanggal: 2024-01-15 14:30:22
Pelanggan: Budi Santoso
Metode Pembayaran: Tunai

Barang Belanja:
ID  Nama                 Qty  Harga (IDR)   Subtotal (IDR)
--  -------------------- ---  -----------  ---------------
 1  Nasi Goreng            2   Rp 12.000       Rp 24.000
 2  Teh Manis              1    Rp 5.000        Rp 5.000

Total Harga:   Rp 29.000
Uang Masuk:    Rp 50.000
Kembalian:     Rp 21.000
```

---

## Code Architecture

The application is built around a single `POS` class. All state (`products` and `cart`) lives as instance variables.

### Method Overview

| Method | Category | Purpose |
|--------|----------|---------|
| `__init__()` | Setup | Initialize `products[]`, `cart[]`, load from CSV |
| `load_products()` | File I/O | Read `products.csv` into products list |
| `save_products()` | File I/O | Write current products list back to CSV |
| `_validate_price()` | Validation | Check if a price string is a valid positive float |
| `list_products()` | Display | Print formatted product table to terminal |
| `add_product()` | Products | Prompt for name & price, append to `products[]` |
| `edit_product()` | Products | Find product by ID, update name/price, save |
| `add_to_cart()` | Cart | Find product by ID, add or accumulate qty in `cart[]` |
| `remove_from_cart()` | Cart | Remove item from `cart[]` by product ID |
| `show_cart()` | Cart | Display cart table with subtotals and grand total |
| `checkout()` | Transaction | Handle full payment flow and call receipt generation |
| `generate_receipt()` | Receipt | Write formatted `.txt` receipt file with timestamp |
| `display_qr_code()` | Payment | Encode payment data as base64 and render QR image |
| `main_menu()` | UI | Render main menu box and capture user choice |
| `run_application()` | App Loop | Main `while` loop — dispatches all actions by choice |

### Application Flow

```
START
  └── POS.__init__()
        └── load_products() ← reads products.csv

  run_application()  [main loop]
  │
  ├── [1] add_product()
  │     ├── validate name & price
  │     ├── append to products[]
  │     └── save_products() → writes products.csv
  │
  ├── [2] edit_product()
  │     ├── list_products()
  │     ├── find by ID
  │     └── save_products()
  │
  ├── [3] list_products()
  │     └── print formatted table
  │
  ├── [4] add_to_cart()
  │     ├── list_products()
  │     ├── find product by ID
  │     └── append or accumulate qty in cart[]
  │
  ├── [5] remove_from_cart()
  │     ├── show_cart()
  │     └── pop item from cart[] by ID
  │
  ├── [6] show_cart()
  │     └── print cart table + grand total
  │
  ├── [7] checkout()
  │     ├── show_cart()
  │     ├── input customer name
  │     ├── choose payment method
  │     │     ├── Tunai → calculate change
  │     │     └── QRIS  → display_qr_code() → confirm
  │     ├── generate_receipt() → saves .txt file
  │     └── cart.clear()
  │
  └── [0] EXIT
```

---

## Dependencies

| Library | Type | Purpose |
|---------|------|---------|
| `os`, `sys` | Built-in | System interaction, stdout flushing |
| `csv` | Built-in | Read and write `products.csv` |
| `json`, `base64` | Built-in | Encode payment data for QR generation |
| `datetime` | Built-in | Timestamps for receipts and filenames |
| `pathlib` | Built-in | File path handling |
| `time` | Built-in | Delays for Colab notebook input stability |
| `io.BytesIO` | Built-in | In-memory buffer for QR image rendering |
| `qrcode[pil]` | **External** | Generate QR code images for QRIS payment |
| `IPython.display` | Colab | Render QR image inline in Colab notebook |

Install external dependency:
```bash
pip install qrcode[pil]
```

---

## Customization

**Edit products manually** — open `products.csv` in any text editor or spreadsheet app. Keep the `id` values as unique integers.

**Change the store name** — search for `"SCHOOL POS"` in `main.py` and replace it with your store name. It appears in the receipt header and main menu.

**Change UI colors** — modify the ANSI color constants at the top of the file:

```python
COLOR_HEADER = '96'   # Bright cyan  → '95' for magenta, '33' for orange
COLOR_MENU   = '93'   # Bright yellow
COLOR_OK     = '92'   # Bright green
COLOR_ERROR  = '91'   # Bright red
```

---

## Limitations

- **Single-user only** — no multi-user or networked access
- **No database** — data stored in plain CSV and TXT files
- **No stock tracking** — quantities are not deducted from inventory
- **No sales history dashboard** — receipts are raw `.txt` files only
- **No authentication** — no login or user accounts
- **QRIS is simulated** — QR links to a demo endpoint, not a real payment gateway
- **Colab-specific workarounds** — `clear_screen()` uses `clear_output()` instead of `os.system('clear')`

---

## License

This project is open source and free to use for educational and personal purposes.

---

<div align="center">
  Made for <strong>UPRAK (Ujian Praktik)</strong> &nbsp;|&nbsp; by <strong>Louie Hansen Linadi</strong>
</div>
