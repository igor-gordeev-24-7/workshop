import psycopg
from config import DB_CONFIG

with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user")
        database, user = cur.fetchone()
        print(database, user)

    with conn.cursor() as cur:
        cur.execute(""" 
            SELECT order_code, customer, device, repair_cost, status
	        FROM workshop_hw.repair_orders
	        ORDER BY id
        """)
        orders = cur.fetchall()



    for order_code, customer, device, repair_cost, status in orders:
        print(
            f"Заказ {order_code} | "
            f"Клиент: {customer} | "
            f"Устройство: {device} | "
            f"Стоимость: {repair_cost} ₽ | "
            f"Статус: {status}"
        )

    with conn.cursor() as cur:
        cur.execute(""" 
            SELECT COUNT(*), SUM(repair_cost)
            FROM workshop_hw.repair_orders
        """)
        total_count, total_sum = cur.fetchone()

    print(f"Всего заказов: {total_count}")
    print(f"Суммарная стоимость: {total_sum} ₽")