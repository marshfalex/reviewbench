def list_products(db, limit: int = 50):
    return db.execute(
        "SELECT id, name, price_cents FROM products ORDER BY name LIMIT ?", (limit,)
    ).fetchall()
