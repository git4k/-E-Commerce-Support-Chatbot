import psycopg2
from langchain.tools import tool
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import DB_CONFIG

@tool
def check_order_status(order_id: str) -> str:
    """Check order status, tracking number, and delivery estimate. Use when customer asks about their order."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_status, o.tracking_number, o.estimated_delivery, c.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        """, (order_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            status, tracking, delivery, name = result
            return f"Order {order_id} for {name}: Status={status}, Tracking={tracking}, Est. Delivery={delivery.strftime('%Y-%m-%d')}"
        return f"Order {order_id} not found."
    except Exception as e:
        return f"Error checking order: {str(e)}"

@tool
def create_refund(order_id: str) -> str:
    """Create a refund request for an order. Use when customer wants to return an item."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO refunds (order_id, status, created_at)
            VALUES (%s, 'pending', NOW())
            RETURNING refund_id
        """, (order_id,))
        refund_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return f"Refund request created. Refund ID: {refund_id}. You will receive an email within 24 hours."
    except Exception as e:
        return f"Error creating refund: {str(e)}"

@tool
def create_support_ticket(customer_id: int, issue_type: str, description: str) -> str:
    """Create a support ticket for complex issues. Use for payment problems, account issues, or escalations."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tickets (customer_id, issue_type, description, status, created_at)
            VALUES (%s, %s, %s, 'open', NOW())
            RETURNING ticket_id
        """, (customer_id, issue_type, description))
        ticket_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return f"Support ticket created. Ticket ID: {ticket_id}. Our team will contact you within 24 hours."
    except Exception as e:
        return f"Error creating ticket: {str(e)}"

@tool
def search_policy_docs(query: str) -> str:
    """Search company policies for return, shipping, and FAQ information. Use for policy questions."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from app.rag.rag_engine import search_policy_docs as search
    return search(query)
