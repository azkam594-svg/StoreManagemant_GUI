from data.database import products, promotions, transactions


# = CONVERT VALUE TO INTEGER
def convert_value_to_int(value):
    try:
        return int(value)
    except:
        return 0


# = GET PRODUCT BY ID FOR STATISTIC
def get_product_by_id_for_statistic(product_id):
    for product in products:
        if str(product["id"]) == str(product_id):
            return True, product

    return False, "Produk tidak ditemukan."


# = GET TRANSACTION QUANTITY
def get_transaction_quantity(transaction):
    if "quantity" in transaction:
        return convert_value_to_int(transaction["quantity"])

    if "qty" in transaction:
        return convert_value_to_int(transaction["qty"])

    return 0


# = GET TRANSACTION AMOUNT
def get_transaction_amount(transaction):
    if "total_price" in transaction:
        return convert_value_to_int(transaction["total_price"])

    if "total" in transaction:
        return convert_value_to_int(transaction["total"])

    if "amount" in transaction:
        return convert_value_to_int(transaction["amount"])

    product_id = transaction.get("product_id")
    quantity = get_transaction_quantity(transaction)

    success, product = get_product_by_id_for_statistic(product_id)

    if not success:
        return 0

    return convert_value_to_int(product["price"]) * quantity


# = TOTAL PRODUCTS
def get_total_products():
    return len(products)


# = TOTAL STOCK
def get_total_stock():
    total_stock = 0

    for product in products:
        total_stock += convert_value_to_int(product["stock"])

    return total_stock


# = TOTAL INVENTORY VALUE
def get_total_inventory_value():
    total_value = 0

    for product in products:
        price = convert_value_to_int(product["price"])
        stock = convert_value_to_int(product["stock"])

        total_value += price * stock

    return total_value


# = TOTAL TRANSACTIONS
def get_total_transactions():
    return len(transactions)


# = TOTAL ITEMS SOLD
def get_total_items_sold():
    total_sold = 0

    for transaction in transactions:
        total_sold += get_transaction_quantity(transaction)

    return total_sold


# = TOTAL SALES REVENUE
def get_total_sales_revenue():
    total_revenue = 0

    for transaction in transactions:
        total_revenue += get_transaction_amount(transaction)

    return total_revenue


# = TOTAL ACTIVE PROMOTIONS
def get_total_active_promotions():
    total_active = 0

    for promotion in promotions:
        if promotion["status"] == "Aktif":
            total_active += 1

    return total_active


# = GET SALES BY PRODUCT
def get_sales_by_product():
    result = []

    for product in products:
        product_id = product["id"]
        product_name = product["name"]

        total_quantity = 0
        total_revenue = 0

        for transaction in transactions:
            if str(transaction.get("product_id")) == str(product_id):
                quantity = get_transaction_quantity(transaction)
                amount = get_transaction_amount(transaction)

                total_quantity += quantity
                total_revenue += amount

        if total_quantity > 0:
            result.append({
                "product_id": product_id,
                "product_name": product_name,
                "total_quantity": total_quantity,
                "total_revenue": total_revenue
            })

    result.sort(key=lambda item: item["total_quantity"], reverse=True)

    return result


# = GET BEST SELLING PRODUCTS
def get_best_selling_products(limit=5):
    sales_data = get_sales_by_product()

    return sales_data[:limit]


# = GET LOW STOCK PRODUCTS
def get_low_stock_products(limit_stock=5):
    result = []

    for product in products:
        stock = convert_value_to_int(product["stock"])

        if stock <= limit_stock:
            result.append({
                "id": product["id"],
                "name": product["name"],
                "category": product["category"],
                "stock": stock,
                "status": product["status"]
            })

    result.sort(key=lambda item: item["stock"])

    return result


# = GET QUANTITY CHART DATA
def get_quantity_chart_data():
    best_selling_products = get_best_selling_products()

    product_names = []
    quantities = []

    for product in best_selling_products:
        product_names.append(product["product_name"])
        quantities.append(product["total_quantity"])

    return product_names, quantities


# = GET REVENUE CHART DATA
def get_revenue_chart_data():
    sales_data = get_sales_by_product()

    product_names = []
    revenues = []

    for product in sales_data:
        product_names.append(product["product_name"])
        revenues.append(product["total_revenue"])

    return product_names, revenues


# = GET STATISTICS SUMMARY
def get_statistics_summary():
    summary = {
        "total_products": get_total_products(),
        "total_stock": get_total_stock(),
        "total_inventory_value": get_total_inventory_value(),
        # "total_transactions": get_total_transactions(),
        # "total_items_sold": get_total_items_sold(),
        # "total_sales_revenue": get_total_sales_revenue(),
        "total_active_promotions": get_total_active_promotions()
    }

    return summary