sql = """
SELECT c.name, c.city, COUNT(o.id) AS orders, COALESCE(SUM(o.amount), 0) AS total
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
GROUP BY c.id
ORDER BY total DESC
"""
for r in con.execute(sql):
    print(f"{r['name']:<12}{r['city']:<13}{r['orders']:>3}{r['total']:>12,.2f}")
