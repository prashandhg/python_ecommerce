def money(value):
    return f"₹{float(value):,.0f}"

def calculate_total(cart, products):
    total = 0
    for product_id, quantity in cart.items():
        match = products[products["id"] == product_id]
        if not match.empty:
            total += float(match.iloc[0]["price"]) * quantity
    return total
