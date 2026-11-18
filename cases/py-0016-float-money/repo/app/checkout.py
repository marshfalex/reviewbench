from .cart import order_total
from .payments_gateway import charge_cents


def checkout(customer_id: str, prices: list[float], tax_rate: float) -> dict:
    total = order_total(prices, tax_rate)
    return charge_cents(customer_id, int(total * 100))
