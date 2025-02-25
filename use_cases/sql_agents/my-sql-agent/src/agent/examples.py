"""
Example queries for training the SQL generation model.
"""
from typing import Dict, Any

EXAMPLE_QUERIES: Dict[str, Dict[str, Any]] = {
    "Get all sales from last month": {
        "query": """
            SELECT s.date, s.sales_amount, s.revenue, s.product_name,
                   c.name as customer_name
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            WHERE s.date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
              AND s.date < DATE_TRUNC('month', CURRENT_DATE)
            ORDER BY s.date DESC
        """,
        "expected_columns": ["date", "sales_amount", "revenue", "product_name", "customer_name"]
    },
    
    "What is the average revenue per customer?": {
        "query": """
            SELECT c.customer_id, c.name,
                   COUNT(s.sale_id) as total_sales,
                   AVG(s.revenue) as avg_revenue,
                   SUM(s.revenue) as total_revenue
            FROM customers c
            LEFT JOIN sales s ON c.customer_id = s.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY avg_revenue DESC
        """,
        "expected_columns": ["customer_id", "name", "total_sales", "avg_revenue", "total_revenue"]
    },
    
    "Show me the top 5 products by sales amount": {
        "query": """
            SELECT p.name as product_name,
                   COUNT(s.sale_id) as number_of_sales,
                   SUM(s.sales_amount) as total_sales_amount,
                   SUM(s.revenue) as total_revenue
            FROM products p
            JOIN sales s ON p.name = s.product_name
            GROUP BY p.name
            ORDER BY total_sales_amount DESC
            LIMIT 5
        """,
        "expected_columns": ["product_name", "number_of_sales", "total_sales_amount", "total_revenue"]
    },
    
    "Which customers haven't made a purchase in the last 3 months?": {
        "query": """
            SELECT c.customer_id, c.name, c.email,
                   MAX(s.date) as last_purchase_date
            FROM customers c
            LEFT JOIN sales s ON c.customer_id = s.customer_id
            GROUP BY c.customer_id, c.name, c.email
            HAVING MAX(s.date) < CURRENT_DATE - INTERVAL '3 months'
               OR MAX(s.date) IS NULL
            ORDER BY last_purchase_date DESC NULLS FIRST
        """,
        "expected_columns": ["customer_id", "name", "email", "last_purchase_date"]
    }
} 