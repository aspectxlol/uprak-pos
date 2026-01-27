# UPRAK-POS

## Overview
UPRAK-POS is a simple, terminal-based Point of Sale (POS) system designed for small businesses, schools, or personal use. It allows users to manage products, handle sales transactions, and generate receipts in a straightforward and user-friendly manner. The system is written in Python and operates entirely in the command line, making it lightweight and easy to run on most computers.

## Features
- **Product Management**: Add, edit, and list products. Products are stored in a CSV file for easy editing and backup.
- **Cart System**: Add products to a cart, adjust quantities, and remove items before checkout.
- **Sales Transactions**: Checkout process calculates totals, accepts payment, and computes change.
- **Receipt Generation**: Automatically generates a text receipt for each transaction, saved with a timestamp.
- **User-Friendly Navigation**: Each screen offers a back/cancel option, allowing users to return to the main menu at any time.
- **Formatted Output**: Uses color-coded text for improved readability in supported terminals.

## How It Works
1. **Main Menu**: Navigate through options to manage products, handle the cart, and process sales.
2. **Product Management**: Add new products with a name and price, edit existing products, or view the product list.
3. **Cart Operations**: Select products to add to the cart, specify quantities, and remove items as needed.
4. **Checkout**: Review the cart, enter the amount of cash received, and the system will calculate change and generate a receipt.
5. **Receipts**: Receipts are saved as text files in the project directory, including all transaction details.

## File Structure
- `main.py`: The main Python script containing all logic for the POS system.
- `products.csv`: Stores product data (ID, name, price).
- `receipt_YYYYMMDD_HHMMSS.txt`: Generated receipts for each transaction.
- `README.md`: This documentation file.

## Usage Instructions
1. Make sure you have Python 3 installed on your system.
2. Run the program from the terminal:
   ```
   python main.py
   ```
3. Follow the on-screen prompts to manage products, add items to the cart, and process sales.
4. Type 'b' at any prompt to cancel the current operation and return to the main menu.

## Customization
- You can edit `products.csv` directly to add or modify products outside the program.
- Receipts are saved in the same directory and can be printed or archived as needed.

## Limitations
- This is a single-user, local POS system. It does not support networking or multi-user access.
- Data is stored in plain text files; there is no database integration.
- Designed for simplicity and educational use, not for large-scale commercial deployment.

## License
This project is open source and free to use for educational and personal purposes.

## Author
Created for UPRAK (Ujian Praktik) and educational demonstration purposes.
Louie Hansen Linadi @