import psycopg2
from datetime import datetime, timedelta
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import DB_CONFIG

def seed_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    statuses = ['processing', 'shipped', 'delivered', 'cancelled']
    
    # SEED 100 ORDERS
    for i in range(101, 201):
        order_id = f"ORD{i}"
        customer_id = random.randint(1, 3)
        status = random.choice(statuses)
        tracking = f"TRK{8000+i}"
        
        cur.execute("""
            INSERT INTO orders (order_id, customer_id, order_status, tracking_number, order_date, estimated_delivery)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (order_id, customer_id, status, tracking, 
              datetime.now() - timedelta(days=random.randint(0,10)),
              datetime.now() + timedelta(days=random.randint(1,5))))
    
    conn.commit()
    print("✅ 100 ORDERS SEEDED!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_data()
