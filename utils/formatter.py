# MEMFORMAT ANGKA KE RP
def format_rupiah(amount):
    """
    Mengubah angka menjadi format Rupiah.

    Contoh:
        8500000 -> Rp 8.500.000
    """

    return f"Rp {amount:,.0f}".replace(",", ".")