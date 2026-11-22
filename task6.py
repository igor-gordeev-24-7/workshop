import psycopg
from config import DB_CONFIG

def check_state(order_code):
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, status FROM workshop_hw.repair_orders
                WHERE order_code = %s
            """,
            (order_code,)
            )
            row = cur.fetchone()
            if row is None:
                return None, None
            order_id, status = row

            cur.execute("""
                SELECT COUNT(*) FROM workshop_hw.order_events
                WHERE order_id = %s
                """,
                (order_id,)
            )

            events = cur.fetchone()[0]
    return status, order_id

status_before, events_before = check_state("RM-101")
print(f"До эксперимента: RM-101 статус = {status_before}, событий = {events_before}")

try:
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE workshop_hw.repair_orders
                SET status = %s
                WHERE order_code = %s AND status = %s
                RETURNING id
                """,
                ("in_progress", "RM-101", "accepted"),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError("RM-101 не в статусе accepted — эксперимент не выполнен")
            order_id = row[0]

            cur.execute("""
                INSERT INTO workshop_hw.order_events (order_id, event_text)
                VALUES (%s, %s)
                """,
                (order_id, None),
            )

except (psycopg.Error, ValueError) as error:
    print(f"Операция отменена: {error.__class__.__name__}: {error}")
else:
    print("Неожиданно: обе операции прошли")


status_after, events_after = check_state("RM-101")
print(f"После эксперимента: RM-101 статус = {status_after}, событий = {events_after}")

status_rm102, events_rm102 = check_state("RM-102")
print(f"RM-102 (из задания 5): статус = {status_rm102}, событий = {events_rm102}")