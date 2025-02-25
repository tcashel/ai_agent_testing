-- Create sample tables for testing MCP SQL Agent

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    inventory_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(12, 2)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL
);

-- Insert sample data
INSERT INTO users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('bob_jones', 'bob@example.com'),
('alice_wong', 'alice@example.com'),
('charlie_brown', 'charlie@example.com');

INSERT INTO products (name, description, price, category, inventory_count) VALUES
('Laptop', 'High-performance laptop with 16GB RAM', 1299.99, 'Electronics', 45),
('Smartphone', '5G smartphone with 128GB storage', 699.99, 'Electronics', 120),
('Coffee Maker', 'Programmable coffee maker with timer', 79.99, 'Kitchen', 35),
('Running Shoes', 'Lightweight running shoes with cushioning', 129.99, 'Footwear', 80),
('Book: SQL Mastery', 'Comprehensive guide to SQL', 49.99, 'Books', 200),
('Wireless Headphones', 'Noise-cancelling wireless headphones', 199.99, 'Electronics', 65),
('Water Bottle', 'Insulated stainless steel water bottle', 24.99, 'Sports', 150),
('Office Chair', 'Ergonomic office chair with lumbar support', 249.99, 'Furniture', 30),
('Protein Powder', 'Whey protein powder, vanilla flavor', 39.99, 'Nutrition', 85),
('Yoga Mat', 'Non-slip yoga mat with carrying strap', 29.99, 'Sports', 100);

-- Create some orders
INSERT INTO orders (user_id, status, total_amount) VALUES
(1, 'completed', 2149.97),
(2, 'completed', 129.99),
(3, 'processing', 249.99),
(4, 'completed', 774.98),
(1, 'pending', 39.99);

-- Add order items
INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 699.99),
(1, 3, 1, 79.99),
(1, 5, 1, 49.99),
(2, 4, 1, 129.99),
(3, 8, 1, 249.99),
(4, 2, 1, 699.99),
(4, 7, 3, 24.99),
(5, 9, 1, 39.99);

-- Create a view for order summaries
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.id AS order_id,
    u.username,
    o.order_date,
    o.status,
    COUNT(oi.id) AS total_items,
    SUM(oi.quantity) AS total_quantity,
    o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.username, o.order_date, o.status, o.total_amount;

-- Create a function to get product sales by category
CREATE OR REPLACE FUNCTION get_sales_by_category()
RETURNS TABLE (
    category VARCHAR,
    total_sales DECIMAL(12, 2),
    item_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.category,
        SUM(oi.quantity * oi.price_per_unit) as total_sales,
        COUNT(DISTINCT p.id) as item_count
    FROM products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
    WHERE o.status = 'completed'
    GROUP BY p.category
    ORDER BY total_sales DESC;
END;
$$ LANGUAGE plpgsql;