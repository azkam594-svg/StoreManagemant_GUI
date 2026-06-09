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
    get_promotion_by_id,
    update_promotion,
    get_all_promotion_histories
    
)


from.transactions_service import (
    calculate_balance,
    export_transactions_csv,
    get_transactions,
    get_transaction_summary,
    record_transaction
)


# =========================
# STATISTICS SERVICE
# =========================
from .statistic_service import (
    get_statistics_summary,
    get_quantity_chart_data,
    get_revenue_chart_data,
    get_promotion_sales_by_product,
    get_recent_transactions,
)