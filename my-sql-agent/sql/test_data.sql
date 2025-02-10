-- Insert test customers
INSERT INTO customers (name, email) VALUES
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Wilson', 'bob@example.com');

-- Insert test products
INSERT INTO products (name, description, price) VALUES
    ('Product A', 'High quality product A', 100.00),
    ('Product B', 'Premium product B', 200.00),
    ('Product C', 'Luxury product C', 300.00);

-- Insert sample sales data for the last 3 months
WITH RECURSIVE dates AS (
    SELECT CURRENT_DATE as date
    UNION ALL
    SELECT date - 3
    FROM dates
    WHERE date > CURRENT_DATE - INTERVAL '3 months'
),
customer_ids AS (
    SELECT customer_id, name FROM customers
),
product_data AS (
    SELECT name, price FROM products
)
INSERT INTO sales (customer_id, date, sales_amount, revenue, product_name)
SELECT 
    c.customer_id,
    d.date,
    (random() * 3 + 1)::int as quantity,
    (random() * 3 + 1)::int * p.price as revenue,
    p.name
FROM dates d
CROSS JOIN customer_ids c
CROSS JOIN product_data p
WHERE d.date <= CURRENT_DATE
ORDER BY d.date DESC; 