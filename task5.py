import psycopg
from config import DB_CONFIG


def complete_repair(order_code):
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE workshop_hw.repair_orders
                    SET status = %s
                    WHERE order_code = %s AND status = %s
                    RETURNING id
                    """,
                    ("ready", order_code, "in_progress"),
                )
                row = cur.fetchone()
                if row is None:
                    raise ValueError(
                        f"Заказ {order_code} не найден или не в статусе in_progress"
                    )
                order_id = row[0]

                cur.execute(
                    """
                    INSERT INTO workshop_hw.order_events (order_id, event_text)
                    VALUES (%s, %s)
                    """,
                    (order_id, "Ремонт завершён"),
                )


    except (psycopg.Error, ValueError) as error:
        print(f"Операция отменена: {error}")
    else:
        print(f"Заказ {order_code} завершён, id = {order_id}")


def show_state(order_code):
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, status FROM workshop_hw.repair_orders
                WHERE order_code = %s
                """,
                (order_code,),
            )
            row = cur.fetchone()
            if row is None:
                print(f"{order_code}: заказ не найден")
                return
            order_id, status = row
            print(row)

            cur.execute("""
                SELECT COUNT(*) FROM workshop_hw.order_events
                WHERE order_id = %s
            """,
            (order_id,),
            )
            events = cur.fetchone()[0]

    print(f"{order_code}: статус = {status}, событий = {events}")



