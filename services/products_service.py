from data.database import products


# == HELPER INTERNAL
# Mengubah input menjadi integer.
def convert_to_int(value): 
    try:
        number = int(value)
        return True, number
    except ValueError:
        return False, "Nilai harus berupa angka."
    except TypeError:
        return False, "Nilai tidak valid."


# Mencari index produk berdasarkan ID.
def find_product_index(product_id):
    success, product_id = convert_to_int(product_id)

    if not success:
        return False, "ID produk harus berupa angka."

    for index, product in enumerate(products):
        if product["id"] == product_id:
            return True, index

    return False, "Produk tidak ditemukan."


# Validasi data produk sebelum ditambahkan atau diedit.
def validate_product_data(name, category, price, stock):
    """ Yang dicek:
    1. Nama produk tidak boleh kosong
    2. Kategori tidak boleh kosong
    3. Harga harus angka
    4. Harga harus lebih dari 0
    5. Stok harus angka
    6. Stok tidak boleh negatif
    """

    if name is None or name.strip() == "":
        return False, "Nama produk tidak boleh kosong."

    if category is None or category.strip() == "":
        return False, "Kategori produk tidak boleh kosong."

    success_price, price = convert_to_int(price)

    if not success_price:
        return False, "Harga produk harus berupa angka."

    success_stock, stock = convert_to_int(stock)

    if not success_stock:
        return False, "Stok produk harus berupa angka."

    if price <= 0:
        return False, "Harga produk harus lebih dari 0."

    if stock < 0:
        return False, "Stok produk tidak boleh negatif."

    clean_data = {
        "name": name.strip(),
        "category": category.strip(),
        "price": price,
        "stock": stock
    }

    return True, clean_data


# Membuat salinan data produk.
def copy_product(product):
    return {
        "id": product["id"],
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "stock": product["stock"],
        "status": product["status"]
    }


# STATUS PRODUK
def get_product_status(stock):
    success, stock = convert_to_int(stock)

    if not success:
        return "Status Tidak Valid"

    if stock <= 0:
        return "Habis"

    if stock <= 5:
        return "Stok Menipis"

    return "Tersedia"


# AMBIL DATA PRODUK
def get_all_products():
    result = []

    for product in products:
        result.append(copy_product(product))

    return result


# Membuat ID produk baru secara otomatis.
def get_next_product_id():
    if len(products) == 0:
        return 1

    highest_id = 0

    for product in products:
        if product["id"] > highest_id:
            highest_id = product["id"]

    return highest_id + 1


# Mengambil satu produk berdasarkan ID.
def get_product_by_id(product_id):
    success, index_or_message = find_product_index(product_id)

    if not success:
        return False, index_or_message

    product = products[index_or_message]

    return True, copy_product(product)




# = BUTTON FUNCTIONS

# TAMBAH PRODUK
def add_product(name, category, price, stock):
    success, result = validate_product_data(
        name=name,
        category=category,
        price=price,
        stock=stock
    )

    if not success:
        return False, result

    clean_data = result

    new_product = {
        "id": get_next_product_id(),
        "name": clean_data["name"],
        "category": clean_data["category"],
        "price": clean_data["price"],
        "stock": clean_data["stock"],
        "status": get_product_status(clean_data["stock"])
    }

    products.append(new_product)

    return True, copy_product(new_product)


# EDIT PRODUK BERDASARKAN ID
def update_product(product_id, name, category, price, stock):

    success, index_or_message = find_product_index(product_id)

    if not success:
        return False, index_or_message

    success, result = validate_product_data(
        name=name,
        category=category,
        price=price,
        stock=stock
    )

    if not success:
        return False, result

    clean_data = result
    index = index_or_message

    products[index]["name"] = clean_data["name"]
    products[index]["category"] = clean_data["category"]
    products[index]["price"] = clean_data["price"]
    products[index]["stock"] = clean_data["stock"]
    products[index]["status"] = get_product_status(clean_data["stock"])

    return True, copy_product(products[index])


# HAPUS PRODUK BERDASARKAN ID
def delete_product(product_id):
    success, index_or_message = find_product_index(product_id)

    if not success:
        return False, index_or_message

    index = index_or_message
    deleted_product = products.pop(index)

    return True, f"Produk '{deleted_product['name']}' berhasil dihapus."


# MENGURANGI STOK PRODUK
def decrease_product_stock(product_id, quantity):
    success, index_or_message = find_product_index(product_id)

    if not success:
        return False, index_or_message

    success_quantity, quantity = convert_to_int(quantity)

    if not success_quantity:
        return False, "Jumlah produk harus berupa angka."

    if quantity <= 0:
        return False, "Jumlah produk harus lebih dari 0."

    index = index_or_message

    if products[index]["stock"] < quantity:
        return False, "Stok produk tidak cukup."

    products[index]["stock"] -= quantity
    products[index]["status"] = get_product_status(products[index]["stock"])

    return True, copy_product(products[index])


# MENAMBAH STOK PRODUK
def increase_product_stock(product_id, quantity):
    success, index_or_message = find_product_index(product_id)

    if not success:
        return False, index_or_message

    success_quantity, quantity = convert_to_int(quantity)

    if not success_quantity:
        return False, "Jumlah produk harus berupa angka."

    if quantity <= 0:
        return False, "Jumlah produk harus lebih dari 0."

    index = index_or_message

    products[index]["stock"] = int(products[index]["stock"]) + quantity
    products[index]["status"] = get_product_status(products[index]["stock"])

    # Kalau kamu pakai JSON/file, aktifkan ini:
    # save_products(products)

    return True, copy_product(products[index])


# PENCARIAN PRODUK
def search_products(keyword):

    if keyword is None or keyword.strip() == "":
        return get_all_products()

    keyword = keyword.lower().strip()

    result = []

    for product in products:
        product_name = product["name"].lower()
        product_category = product["category"].lower()

        if keyword in product_name or keyword in product_category:
            result.append(copy_product(product))

    return result





# == STATISTIK PRODUK

# Menghitung jumlah jenis produk.
def get_total_products():
    return len(products)

# Menghitung total seluruh stok produk.
def get_total_stock():
    total = 0

    for product in products:
        total += product["stock"]

    return total

# Menghitung total nilai inventori.
def get_total_inventory_value():
    total = 0

    for product in products:
        total += product["price"] * product["stock"]

    return total

# Mengambil produk dengan stok paling sedikit.
def get_low_stock_products(limit_stock=5):
    success, limit = convert_to_int(limit_stock)

    if not success:
        limit_stock = 5

    result = []

    for product in products:
        if product["stock"] <= limit_stock:
            result.append(copy_product(product))

    return result