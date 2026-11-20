import psycopg
from config import DB_CONFIG

order_code = input("Введите код заказа: ").strip()

with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT customer, device, repair_cost, status
            FROM workshop_hw.repair_orders
            WHERE order_code = %s
            """,
            (order_code,)
        )
        row = cur.fetchone()

    if row is None:
        print("Заказ не найден")
    else:
        customer, device, repair_cost, status = row
        print(f"Клиент: {customer}")
        print(f"Устройство: {device}")
        print(f"Стоимость: {repair_cost} ₽")
        print(f"Статус: {status}")

status = "accepted"
max_cost = 2000

with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT order_code, customer, device, repair_cost, status
            FROM workshop_hw.repair_orders
            WHERE status = %s and repair_cost <= %s
            ORDER BY id
            """,
            (status, max_cost)
        )
        row = cur.fetchall()

    print(f"\nЗаказы со статусом '{status}' и стоимостью ≤ {max_cost} ₽:")
    for order_code, customer, device, repair_cost, status_ in row:
        print(
            f"Заказ {order_code} | "
            f"Клиент: {customer} | "
            f"Устройство: {device} | "
            f"Стоимость: {repair_cost} ₽ | "
            f"Статус: {status}"
        )
