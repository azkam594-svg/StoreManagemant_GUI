from data.database import transactions, products
import csv
from datetime import datetime


def get_product_by_sku(sku):
    return next((p for p in products if p.get("sku") == sku), None)


def get_transaction_amount(transaction):
    product = get_product_by_sku(transaction.get("sku"))
    if product is None:
        return 0

    return product.get("price", 0) * transaction.get("quantity", 0)


def get_transactions():
    return transactions


def get_transaction_summary():
    masuk = sum(1 for t in transactions if t.get("type") == "Masuk")
    keluar = sum(1 for t in transactions if t.get("type") == "Keluar")
    total = len(transactions)
    total_sales = sum(
        get_transaction_amount(t)
        for t in transactions
        if t.get("type") == "Keluar"
    )

    return {
        "masuk": masuk,
        "keluar": keluar,
        "total": total,
        "total_sales": total_sales,
    }


# =========================
# HITUNG TOTAL SALDO
# =========================
def calculate_balance():
    summary = get_transaction_summary()
    return summary["total_sales"]


# =========================
# CATAT TRANSAKSI
# =========================
def record_transaction(sku, quantity, transaction_type):
    product = get_product_by_sku(sku)
    if product is None:
        raise ValueError("SKU tidak ditemukan")

    if quantity <= 0:
        raise ValueError("Jumlah transaksi harus lebih besar dari 0")

    if transaction_type == "Keluar":
        if product.get("stock", 0) < quantity:
            raise ValueError("Stok tidak cukup untuk penjualan")
        product["stock"] -= quantity
    elif transaction_type == "Masuk":
        product["stock"] += quantity
    else:
        raise ValueError("Tipe transaksi harus Masuk atau Keluar")

    new_id = transactions[-1]["id"] + 1 if transactions else 1
    new_transaction = {
        "id": new_id,
        "sku": sku,
        "quantity": quantity,
        "type": transaction_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    transactions.append(new_transaction)
    return new_transaction


# =========================
# EXPORT KE CSV
# =========================
def export_transactions_csv(filename="transactions.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["ID", "SKU", "Tipe", "Quantity", "Amount", "Date"])

        for t in transactions:
            writer.writerow([
                t.get("id"),
                t.get("sku"),
                t.get("type"),
                t.get("quantity"),
                get_transaction_amount(t),
                t.get("date"),
            ])

    return filename