from data.database import transactions, products, promotions
from .products_service import get_product_status
import csv
from datetime import datetime



# CONVERT TO INTEGER

def convert_to_int(value):
    try:
        return True, int(value)
    except:
        return False, value


# GET PRODUCT BY ID

def get_product_by_id(product_id):
    success, product_id = convert_to_int(product_id)

    if not success:
        return False, "ID produk harus berupa angka."

    for product in products:
        if product["id"] == product_id:
            return True, product

    return False, "Produk tidak ditemukan."


# GET ACTIVE PROMOTION BY PRODUCT ID

def get_active_promotion_by_product_id(product_id):
    success, product_id = convert_to_int(product_id)

    if not success:
        return None

    for promotion in promotions:
        if (
            promotion["product_id"] == product_id
            and promotion["status"] == "Aktif"
        ):
            return promotion

    return None


# CALCULATE FINAL PRICE

def calculate_final_price(price, discount_percent):
    discount_value = price * discount_percent / 100
    final_price = price - discount_value

    return int(final_price)


# GET NEXT TRANSACTION ID

def get_next_transaction_id():
    if len(transactions) == 0:
        return 1

    highest_id = 0

    for transaction in transactions:
        if transaction["id"] > highest_id:
            highest_id = transaction["id"]

    return highest_id + 1



# COPY TRANSACTION WITH PRODUCT

def copy_transaction_with_product(transaction):
    success, product = get_product_by_id(transaction["product_id"])

    if not success:
        return {
            "id": transaction["id"],
            "product_id": transaction["product_id"],
            "product_name": "Produk tidak ditemukan",
            "category": "-",
            "quantity": transaction["quantity"],
            "type": transaction["type"],
            "price": transaction.get("price", 0),
            "discount_percent": transaction.get("discount_percent", 0),
            "final_price": transaction.get("final_price", 0),
            "total_price": transaction.get("total_price", 0),
            "date": transaction["date"],
            "status": transaction.get("status", "Selesai")
        }

    return {
        "id": transaction["id"],
        "product_id": transaction["product_id"],
        "product_name": product["name"],
        "category": product["category"],
        "quantity": transaction["quantity"],
        "type": transaction["type"],
        "price": transaction.get("price", 0),
        "discount_percent": transaction.get("discount_percent", 0),
        "final_price": transaction.get("final_price", 0),
        "total_price": transaction.get("total_price", 0),
        "date": transaction["date"],
        "status": transaction.get("status", "Selesai")
    }



# GET TRANSACTION AMOUNT

def get_transaction_amount(transaction):
    return transaction.get("total_price", 0)


# GET TRANSACTIONS

def get_transactions():
    result = []

    for transaction in transactions:
        result.append(copy_transaction_with_product(transaction))

    return result



# GET TRANSACTION SUMMARY

def get_transaction_summary():
    masuk = 0
    keluar = 0
    total_sales = 0
    total_expense = 0

    for transaction in transactions:
        if transaction.get("type") == "Masuk":
            masuk += 1
            total_expense += get_transaction_expense(transaction)

        elif transaction.get("type") == "Keluar":
            keluar += 1
            total_sales += get_transaction_amount(transaction)

    return {
        "masuk": masuk,
        "keluar": keluar,
        "total": len(transactions),
        "total_sales": total_sales,
        "total_expense": total_expense,
        "net_balance": total_sales - total_expense
    }


# GET TRANSACTION EXPENSE

def get_transaction_expense(transaction):
    if transaction.get("type") != "Masuk":
        return 0

    if "total_price" in transaction and transaction.get("total_price", 0) > 0:
        return transaction.get("total_price", 0)

    price = transaction.get("price", 0)
    quantity = transaction.get("quantity", 0)

    return price * quantity


# CALCULATE BALANCE

def calculate_balance():
    summary = get_transaction_summary()

    return summary["net_balance"]



# WRITE TRANSACTION

def record_transaction(product_id, quantity, transaction_type):
    success_product, product = get_product_by_id(product_id)

    if not success_product:
        raise ValueError(product)

    success_quantity, quantity = convert_to_int(quantity)

    if not success_quantity:
        raise ValueError("Jumlah transaksi harus berupa angka.")

    if quantity <= 0:
        raise ValueError("Jumlah transaksi harus lebih besar dari 0.")

    if transaction_type not in ["Masuk", "Keluar"]:
        raise ValueError("Tipe transaksi harus Masuk atau Keluar.")

    product_id = product["id"]
    price = product["price"]

    discount_percent = 0
    final_price = price
    total_price = 0

    if transaction_type == "Keluar":
        if product["stock"] < quantity:
            raise ValueError("Stok tidak cukup untuk penjualan.")

        active_promotion = get_active_promotion_by_product_id(product_id)

        if active_promotion is not None:
            discount_percent = active_promotion["discount_percent"]
            final_price = calculate_final_price(price, discount_percent)

        total_price = final_price * quantity

        product["stock"] -= quantity
        product["status"] = get_product_status(product["stock"])

    elif transaction_type == "Masuk":
        total_price = price * quantity
        product["stock"] += quantity
        product["status"] = get_product_status(product["stock"])

    new_transaction = {
        "id": get_next_transaction_id(),
        "product_id": product_id,
        "quantity": quantity,
        "type": transaction_type,
        "price": price,
        "discount_percent": discount_percent,
        "final_price": final_price,
        "total_price": total_price,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Selesai"
    }

    transactions.append(new_transaction)

    return copy_transaction_with_product(new_transaction)


# EXPORT TO CSV

def export_transactions_csv(filename="transactions.csv"):
    transaction_list = get_transactions()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Product ID",
            "Product Name",
            "Category",
            "Tipe",
            "Quantity",
            "Harga Asli",
            "Diskon",
            "Harga Akhir",
            "Total",
            "Tanggal",
            "Status"
        ])

        for transaction in transaction_list:
            writer.writerow([
                transaction["id"],
                transaction["product_id"],
                transaction["product_name"],
                transaction["category"],
                transaction["type"],
                transaction["quantity"],
                transaction["price"],
                transaction["discount_percent"],
                transaction["final_price"],
                transaction["total_price"],
                transaction["date"],
                transaction["status"]
            ])

    return filename