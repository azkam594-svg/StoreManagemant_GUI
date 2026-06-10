from data.database import products, promotions, transactions

# from utils.formatter import format_rupiah

# CONVERT VALUE TO INTEGER

def convert_value_to_int(value):
    try:
        return int(value)
    except:
        return 0



# GET PRODUCT BY ID

def get_product_by_id(product_id):
    product_id = convert_value_to_int(product_id)

    for product in products:
        if product["id"] == product_id:
            return True, product

    return False, "Produk tidak ditemukan."



# GET TRANSACTION QUANTITY

def get_transaction_quantity(transaction):
    return convert_value_to_int(transaction.get("quantity", 0))



# GET TRANSACTION AMOUNT

def get_transaction_amount(transaction):
    if transaction.get("type") != "Keluar":
        return 0

    if "total_price" in transaction:
        return convert_value_to_int(transaction.get("total_price", 0))

    quantity = get_transaction_quantity(transaction)
    final_price = convert_value_to_int(transaction.get("final_price", 0))
    price = convert_value_to_int(transaction.get("price", 0))

    if final_price > 0:
        return final_price * quantity

    return price * quantity


# AVERAGE PRODUCT PRICE

def get_average_product_price():
    if len(products) == 0:
        return 0

    total_price = 0

    for product in products:
        total_price += convert_value_to_int(product.get("price", 0))

    return int(total_price / len(products))



# HIGHEST INVENTORY VALUE PRODUCT

def get_highest_inventory_value_product():
    if len(products) == 0:
        return {
            "name": "-",
            "inventory_value": 0
        }

    highest_product = products[0]
    highest_value = (
        convert_value_to_int(highest_product.get("price", 0))
        * convert_value_to_int(highest_product.get("stock", 0))
    )

    for product in products:
        price = convert_value_to_int(product.get("price", 0))
        stock = convert_value_to_int(product.get("stock", 0))
        inventory_value = price * stock

        if inventory_value > highest_value:
            highest_value = inventory_value
            highest_product = product

    return {
        "name": highest_product.get("name", "-"),
        "inventory_value": highest_value
    }



# TOTAL ACTIVE PROMOTIONS

def get_total_active_promotions():
    total_active = 0

    for promotion in promotions:
        if promotion.get("status") == "Aktif":
            total_active += 1

    return total_active



# PROMOTION SALES SUMMARY

def get_promotion_sales_summary():
    total_promo_transactions = 0
    total_promo_items_sold = 0
    total_promo_revenue = 0
    total_discount_given = 0

    for transaction in transactions:
        if transaction.get("type") != "Keluar":
            continue

        discount_percent = convert_value_to_int(
            transaction.get("discount_percent", 0)
        )

        if discount_percent <= 0:
            continue

        quantity = get_transaction_quantity(transaction)
        price = convert_value_to_int(transaction.get("price", 0))
        final_price = convert_value_to_int(transaction.get("final_price", 0))
        total_price = get_transaction_amount(transaction)

        discount_value = (price - final_price) * quantity

        total_promo_transactions += 1
        total_promo_items_sold += quantity
        total_promo_revenue += total_price
        total_discount_given += discount_value

    return {
        "total_promo_transactions": total_promo_transactions,
        "total_promo_items_sold": total_promo_items_sold,
        "total_promo_revenue": total_promo_revenue,
        "total_discount_given": total_discount_given
    }



# TOTAL SALES REVENUE

def get_total_sales_revenue():
    total_revenue = 0

    for transaction in transactions:
        total_revenue += get_transaction_amount(transaction)

    return total_revenue



# TOTAL ITEMS SOLD

def get_total_items_sold():
    total_sold = 0

    for transaction in transactions:
        if transaction.get("type") == "Keluar":
            total_sold += get_transaction_quantity(transaction)

    return total_sold



# SALES BY PRODUCT

def get_sales_by_product():
    result = []

    for product in products:
        product_id = product["id"]
        product_name = product["name"]
        category = product.get("category", "-")

        total_quantity = 0
        total_revenue = 0

        for transaction in transactions:
            if transaction.get("type") != "Keluar":
                continue

            if convert_value_to_int(transaction.get("product_id")) != product_id:
                continue

            quantity = get_transaction_quantity(transaction)
            amount = get_transaction_amount(transaction)

            total_quantity += quantity
            total_revenue += amount

        if total_quantity > 0:
            result.append({
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "total_quantity": total_quantity,
                "total_revenue": total_revenue
            })

    result.sort(key=lambda item: item["total_quantity"], reverse=True)

    return result



# QUANTITY CHART DATA

def get_quantity_chart_data(limit=5):
    sales_data = get_sales_by_product()
    sales_data = sales_data[:limit]

    product_names = []
    quantities = []

    for product in sales_data:
        product_names.append(product["product_name"])
        quantities.append(product["total_quantity"])

    return product_names, quantities



# REVENUE CHART DATA

def get_revenue_chart_data(limit=5):
    sales_data = get_sales_by_product()
    sales_data.sort(key=lambda item: item["total_revenue"], reverse=True)
    sales_data = sales_data[:limit]

    product_names = []
    revenues = []

    for product in sales_data:
        product_names.append(product["product_name"])
        revenues.append(product["total_revenue"])

    return product_names, revenues



# PROMOTION SALES BY PRODUCT

def get_promotion_sales_by_product():
    result = []

    for promotion in promotions:
        product_id = convert_value_to_int(promotion.get("product_id"))
        discount_percent = convert_value_to_int(
            promotion.get("discount_percent", 0)
        )

        success, product = get_product_by_id(product_id)

        if success:
            product_name = product.get("name", "-")
            category = product.get("category", "-")
        else:
            product_name = "Produk tidak ditemukan"
            category = "-"

        total_quantity = 0
        total_revenue = 0
        total_discount = 0

        for transaction in transactions:
            if transaction.get("type") != "Keluar":
                continue

            if convert_value_to_int(transaction.get("product_id")) != product_id:
                continue

            transaction_discount = convert_value_to_int(
                transaction.get("discount_percent", 0)
            )

            if transaction_discount <= 0:
                continue

            quantity = get_transaction_quantity(transaction)
            price = convert_value_to_int(transaction.get("price", 0))
            final_price = convert_value_to_int(transaction.get("final_price", 0))
            total_price = get_transaction_amount(transaction)

            total_quantity += quantity
            total_revenue += total_price
            total_discount += (price - final_price) * quantity

        result.append({
            "promotion_id": promotion.get("id"),
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "discount_percent": discount_percent,
            "total_quantity": total_quantity,
            "total_revenue": total_revenue,
            "total_discount": total_discount,
            "status": promotion.get("status", "-")
        })

    result.sort(key=lambda item: item["total_revenue"], reverse=True)

    return result


# RECENT TRANSACTIONS

def get_recent_transactions(limit=5):
    result = []

    for transaction in transactions:
        success, product = get_product_by_id(transaction.get("product_id"))

        if success:
            product_name = product.get("name", "-")
        else:
            product_name = "Produk tidak ditemukan"

        result.append({
            "id": transaction.get("id"),
            "product_id": transaction.get("product_id"),
            "product_name": product_name,
            "type": transaction.get("type"),
            "quantity": transaction.get("quantity"),
            "total_price": get_transaction_amount(transaction),
            "date": transaction.get("date"),
            "status": transaction.get("status", "-")
        })

    result.sort(
        key=lambda item: convert_value_to_int(item.get("id")),
        reverse=True
    )

    return result[:limit]



# STATISTICS SUMMARY

def get_statistics_summary():
    promotion_summary = get_promotion_sales_summary()

    return {
        # Product
        "average_product_price": get_average_product_price(),
        "highest_inventory_value_product": get_highest_inventory_value_product(),

        # Promotion
        "total_active_promotions": get_total_active_promotions(),
        "promotion_summary": promotion_summary,

        # Transaction
        "total_sales_revenue": get_total_sales_revenue(),
        "total_items_sold": get_total_items_sold()
    }