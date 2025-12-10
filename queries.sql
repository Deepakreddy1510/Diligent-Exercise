-- queries.sql

-- 1) Order totals (join order_items and orders, group by order)
SELECT
  o.order_id,
  o.customer_id,
  o.order_date,
  o.status,
  SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY order_total DESC
LIMIT 10;

-- 2) Top customers by total spend
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
  COUNT(DISTINCT o.order_id) AS orders_count,
  SUM(oi.quantity * oi.unit_price) AS total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id
ORDER BY total_spend DESC
LIMIT 10;

-- 3) Product-level sales and average rating (join with reviews)
SELECT
  p.product_id,
  p.name,
  p.category,
  SUM(oi.quantity) AS total_units_sold,
  SUM(oi.quantity * oi.unit_price) AS revenue,
  AVG(r.rating) AS average_rating,
  COUNT(r.review_id) AS review_count
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 20;

-- 4) Recent orders with customer email and a list of products in the order
SELECT 
  o.order_id,
  o.order_date,
  c.email,
  group_concat(p.name, '; ') AS product_names,
  SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_date DESC
LIMIT 20;
