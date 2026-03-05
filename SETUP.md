# 📋 Detailed Setup Guide

## Step 1: PostgreSQL Setup

### Install PostgreSQL
Download and install PostgreSQL 18 from https://www.postgresql.org/download/

### Create Database
```sql
CREATE DATABASE ecommerce_support;
```

### Create Tables
```sql
-- Connect to ecommerce_support database first

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id INT,
    order_status TEXT,
    tracking_number TEXT,
    order_date TIMESTAMP,
    estimated_delivery TIMESTAMP
);

CREATE TABLE refunds (
    refund_id SERIAL PRIMARY KEY,
    order_id TEXT,
    status TEXT,
    created_at TIMESTAMP
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    customer_id INT,
    issue_type TEXT,
    description TEXT,
    status TEXT,
    created_at TIMESTAMP
);
```

### Insert Sample Customers
```sql
INSERT INTO customers (name, email, created_at) VALUES
('Jane Smith', 'jane@example.com', NOW()),
('John Doe', 'john@example.com', NOW()),
('Bob Wilson', 'bob@example.com', NOW());
```

## Step 2: Get Groq API Key

1. Go to https://console.groq.com
2. Sign up (free)
3. Navigate to API Keys
4. Create new API key
5. Copy the key (starts with `gsk_`)

## Step 3: Configure Application

1. Copy the example config:
```bash
cp config.example.py config.py
```

2. Edit `config.py`:
```python
GROQ_API_KEY = "gsk_YOUR_ACTUAL_KEY_HERE"

DB_CONFIG = {
    "dbname": "ecommerce_support",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD",
    "host": "localhost"
}
```

## Step 4: Seed Database

Run the seeder to create 100 sample orders:
```bash
python app/db/seed_data.py
```

You should see: `✅ 100 ORDERS SEEDED!`

## Step 5: Run Application

```bash
streamlit run streamlit_app_simple.py
```

The app will open at http://localhost:8501

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL service is running
- Check username/password in config.py
- Ensure database exists

### Module Not Found Error
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Groq API Error
- Verify API key is correct
- Check internet connection
- Ensure you're using a valid model name

### Slow First Response
- First query loads embeddings model (~5-10 seconds)
- Subsequent queries are fast (~0.3-0.5 seconds)
- This is normal behavior

## Testing

Try these queries:
- "Where is my order ORD101?"
- "What is your return policy?"
- "I want to return order ORD150"
- "My payment failed"

## Performance

- First query: 5-10 seconds (loading models)
- Subsequent queries: 0.3-0.5 seconds
- Database queries: <100ms
- RAG search: Cached after first use
