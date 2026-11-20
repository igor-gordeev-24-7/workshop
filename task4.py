from decimal import Decimal

import psycopg
from config import DB_CONFIG

conn = psycopg.connect(**DB_CONFIG)
try:
    # 1. UPDATE
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE workshop_hw.repair_orders
            SET repair_cost = %s 
            WHERE order_code = %s
        """,
        (Decimal("4000.00"), "RM-105"),
        )

    with conn.cursor() as cur:
        cur.execute("""
        SELECT repair_cost FROM workshop_hw.repair_orders
        WHERE order_code = %s
        """,
        ("RM-105",),
        )
        cost_after_update = cur.fetchone()[0]
    print("После UPDATE:", cost_after_update)

    conn.rollback()

    with conn.cursor() as cur:
        cur.execute("""
        SELECT repair_cost FROM workshop_hw.repair_orders
        WHERE order_code = %s
        """,
        ("RM-105",),
        )
        cost_after_update = cur.fetchone()[0]
    print("После ROLLBACK:", cost_after_update)

    conn.commit()

except Exception:
    conn.rollback()
    raise
finally:
    conn.close()