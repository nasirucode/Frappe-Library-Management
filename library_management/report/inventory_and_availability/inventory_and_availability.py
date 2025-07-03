import frappe

def execute(filters=None):
    columns = [
        {"label": "Book Title", "fieldname": "book_title", "fieldtype": "Data", "width": 200},
        {"label": "Location", "fieldname": "location", "fieldtype": "Data", "width": 150},
        {"label": "Total Copies", "fieldname": "total", "fieldtype": "Int", "width": 100},
        {"label": "Available Copies", "fieldname": "available", "fieldtype": "Int", "width": 120},
        {"label": "Borrowed Copies", "fieldname": "borrowed", "fieldtype": "Int", "width": 120},
        {"label": "Lost/Damaged Copies", "fieldname": "lost", "fieldtype": "Int", "width": 130},
    ]

    data = frappe.db.sql("""
        SELECT 
            bt.title AS book_title,
            b.location AS location,
            COUNT(b.name) AS total,
            SUM(CASE WHEN b.status = 'Available' THEN 1 ELSE 0 END) AS available,
            SUM(CASE WHEN b.status = 'Issued' THEN 1 ELSE 0 END) AS borrowed,
            SUM(CASE WHEN b.status IN ('Lost', 'Damaged') THEN 1 ELSE 0 END) AS lost
        FROM `tabBook` b
        LEFT JOIN `tabBook Title` bt ON b.book_title = bt.name
        GROUP BY b.book_title, b.location
        ORDER BY bt.title, b.location
    """, as_dict=True)

    return columns, data
