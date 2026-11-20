import psycopg
from config import DB_CONFIG

with psycopg.connect(**DB_CONFIG) as conn:
    # with conn.cursor() as cur:
    #     cur.execute("""
    #         INSERT INTO workshop_hw.repair_orders(
    #     	order_code, customer, device, repair_cost)
    #     	VALUES (%s, %s, %s, %s)
    #     	RETURNING id;
    #     """,
    #     ('RM - 105', 'Денис', 'Принтер', 3500.50)
    #     )
    #     new_id = cur.fetchone()[0]
    # print(f"Заказ сохранён, id = {new_id}")

    status = "accepted"
    repair_cost = 3500.50
    with conn.cursor() as cur:
        cur.execute("""  
            SELECT order_code, customer, device, repair_cost, status
	        FROM workshop_hw.repair_orders
	        WHERE status = %s AND repair_cost = %s
	        ORDER BY id
        """,
        (status, repair_cost)
        )

        orders = cur.fetchall()

        for order_code, customer, device, repair_cost, status in orders:
            print(
                f"Заказ {order_code} | "
                f"Клиент: {customer} | "
                f"Устройство: {device} | "
                f"Стоимость: {repair_cost} ₽ | "
                f"Статус: {status}"
            )


