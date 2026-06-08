from .products_service import (
    get_all_products,
    get_next_product_id,
    get_product_by_id,
    add_product,
    search_products,
    update_product,
    delete_product,
    decrease_product_stock,
    increase_product_stock,
    get_product_status,
    convert_to_int,

    
    # STATISTICS
    get_total_products,
    get_total_stock,
    get_total_inventory_value,
    get_low_stock_products
)



from .promotions_service import (
    search_promotions,
    get_all_promotions,
    add_promotion,
    delete_promotion,
    calculate_discount_price,
    get_promotion_by_id,
    update_promotion,
    get_all_promotion_histories
    
)