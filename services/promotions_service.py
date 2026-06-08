from data.database import promotions, promotion_histories
from datetime import datetime
from services.products_service import get_product_by_id, convert_to_int



# COPY FROM PRUDUCTS FOR TABLE PROMOTIONS 
def copy_promotion_with_price(promotion):
    success, product = get_product_by_id(promotion["product_id"])

    if not success:
        return {
            "id": promotion["id"],
            "product_id": promotion["product_id"],
            "product_name": "Produk tidak ditemukan",
            "category": "-",
            "original_price": 0,
            "discount_percent": promotion["discount_percent"],
            "final_price": 0,
            "status": promotion["status"]
        }

    original_price = product["price"]
    discount_percent = promotion["discount_percent"]
    final_price = calculate_discount_price(original_price, discount_percent)

    return {
        "id": promotion["id"],
        "product_id": promotion["product_id"],
        "product_name": product["name"],
        "category": product["category"],
        "original_price": original_price,
        "discount_percent": discount_percent,
        "final_price": final_price,
        "status": promotion["status"]
    }


def get_next_promotion_id():
    if len(promotions) == 0:
        return 1

    highest_id = 0

    for promotion in promotions:
        if promotion["id"] > highest_id:
            highest_id = promotion["id"]

    return highest_id + 1


def get_next_promotion_history_id():
    if len(promotion_histories) == 0:
        return 1
    
    highest_id = 0
    
    for history in promotion_histories:
        if history["id"] > highest_id:
            highest_id = history["id"]
    
    return highest_id + 1


# ADD PROMOTION HIETORIES
def add_promotion_history(action, promotion_id, product_id,old_discount, new_discount, status):
    history = {
        "id": get_next_promotion_history_id(),
        "promotion_id": promotion_id,
        "product_id": product_id,
        "action": action,
        "old_discount": old_discount,
        "new_discount": new_discount,
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    promotion_histories.append(history)
    return history


# GET ALL HISTORIES
def get_all_promotion_histories():
    return promotion_histories
    

# PROSSES CALCULATE DISCOUNT
def calculate_discount_price(original_price, discount_percent):
    discount_value = original_price * discount_percent / 100
    final_price = original_price - discount_value

    return int(final_price)


# STATUS PROMOTION
def product_has_active_promotion(product_id):
    success, product_id = convert_to_int(product_id)

    if not success:
        return False

    for promotion in promotions:
        if promotion["product_id"] == product_id and promotion["status"] == "Aktif":
            return True

    return False


def get_all_promotions():
    result = []
    
    for promotion in promotions:
        result.append(copy_promotion_with_price(promotion))
        
    return result


# FIND PROMOTION INDEX BY ID
def find_promotion_index(promotion_id):
    success, promotion_id = convert_to_int(promotion_id)

    if not success:
        return False, "ID promosi harus berupa angka."

    for index, promotion in enumerate(promotions):
        if promotion["id"] == promotion_id:
            return True, index

    return False, "Promosi tidak ditemukan."


# GET PROMOTIOON BY ID
def get_promotion_by_id(promotion_id):
    success, index_or_message = find_promotion_index(promotion_id)

    if not success:
        return False, index_or_message

    index = index_or_message
    promotion = promotions[index]

    return True, copy_promotion_with_price(promotion)



# = BUTTON FUNCTIONS

# ADD PROMOTION
def add_promotion(product_id, discount_percent):
    success_product_id, product_id = convert_to_int(product_id)

    if not success_product_id:
        return False, "ID produk harus berupa angka."

    success_product, product = get_product_by_id(product_id)

    if not success_product:
        return False, "Product tidak ditemukan"

    success_discount, discount_percent = convert_to_int(discount_percent)

    if not success_discount:
        return False, "Diskon harus berupa angka."

    if discount_percent <= 0:
        return False, "Diskon harus lebih dari 0%."

    if discount_percent > 100:
        return False, "Diskon tidak boleh lebih dari 100%."

    if product_has_active_promotion(product_id):
        return False, "Produk ini sudah memiliki promosi aktif."

    new_promotion = {
        "id": get_next_promotion_id(),
        "product_id": product_id,
        "discount_percent": discount_percent,
        "status": "Aktif"
    }

    promotions.append(new_promotion)
    
    add_promotion_history(
        action= "Tambah",
        promotion_id= new_promotion["id"],
        product_id= product_id,
        old_discount= 0,
        new_discount= discount_percent,
        status= "Aktif"
    )

    return True, copy_promotion_with_price(new_promotion)


# DELETE PROMOTION
def delete_promotion(promotion_id):
    success, promotion_id = convert_to_int(promotion_id)

    if not success:
        return False, "ID promosi harus berupa angka."

    for index, promotion in enumerate(promotions):
        if promotion["id"] == promotion_id:
            deleted_promotion = promotions.pop(index)
            
            add_promotion_history(
                action="Hapus",
                promotion_id=deleted_promotion["id"],
                product_id=deleted_promotion["product_id"],
                old_discount=deleted_promotion["discount_percent"],
                new_discount=0,
                status="Dihapus"
            )
            
            return True, f"Promosi ID {deleted_promotion['id']} berhasil dihapus."

    return False, "Promosi tidak ditemukan."


# SEARCH PROMOTION
def search_promotions(keyword):
    if keyword is None or keyword.strip() == "":
        return get_all_promotions()
    
    keyword = keyword.lower().strip()
    
    result = []
    
    promotion_list = get_all_promotions()
    
    for promotion in promotion_list:
        promotion_name = (promotion.get("product_name", "")).lower()
        promotion_category = (promotion.get("category", "")).lower()
        
        if keyword in promotion_name or keyword in promotion_category:
            result.append(promotion)
            
    return result


# EDIT PROMOTION
def update_promotion(promotion_id, discount_percent):
    success, promotion_id = convert_to_int(promotion_id)

    if not success:
        return False, "ID promosi harus berupa angka."

    success_discount, discount_percent = convert_to_int(discount_percent)

    if not success_discount:
        return False, "Diskon harus berupa angka."

    if discount_percent <= 0:
        return False, "Diskon harus lebih dari 0%."

    if discount_percent > 100:
        return False, "Diskon tidak boleh lebih dari 100%."

    success, index_or_message = find_promotion_index(promotion_id)

    if not success:
        return False, index_or_message

    index = index_or_message
    
    old_discount = promotions[index]["discount_percent"]
    
    promotions[index]["discount_percent"] = discount_percent
    
    add_promotion_history(
        action= "Edit",
        promotion_id=promotions[index]["id"],
        product_id=promotions[index]["product_id"],
        old_discount=old_discount,
        new_discount=discount_percent,
        status=promotions[index]["status"]
    )
    

    # # Update data asli di list promotions
    # promotions[index]["discount_percent"] = discount_percent

    # Return data copy untuk ditampilkan
    updated_promotion = copy_promotion_with_price(promotions[index])

    return True, updated_promotion