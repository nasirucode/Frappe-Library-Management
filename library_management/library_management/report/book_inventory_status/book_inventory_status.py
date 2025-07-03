import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    
    # Set up columns
    columns = get_columns(filters)
    
    # Get data based on filters
    data = get_data(filters)
    
    # Add summary row if grouped by title
    if not filters.show_individual_books:
        data = add_summary_row(data)
    
    return columns, data

def get_columns(filters):
    """Return columns based on whether showing individual books or grouped"""
    if filters.get("show_individual_books"):
        return [
            {"label": _("Book Code"), "fieldname": "book_code", "fieldtype": "Link", "options": "Book", "width": 120},
            {"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Link", "options": "Book Title", "width": 200},
            {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
            {"label": _("Location"), "fieldname": "location", "fieldtype": "Data", "width": 150},
            {"label": _("Shelf"), "fieldname": "shelf", "fieldtype": "Data", "width": 100},
            {"label": _("Condition"), "fieldname": "condition", "fieldtype": "Data", "width": 100},
        ]
    else:
        return [
            {"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Link", "options": "Book Title", "width": 250},
            {"label": _("Total Copies"), "fieldname": "total", "fieldtype": "Int", "width": 100},
            {"label": _("Available"), "fieldname": "available", "fieldtype": "Int", "width": 100},
            {"label": _("Borrowed"), "fieldname": "borrowed", "fieldtype": "Int", "width": 100},
            {"label": _("Lost/Damaged"), "fieldname": "lost_damaged", "fieldtype": "Int", "width": 120},
            {"label": _("Availability %"), "fieldname": "availability_percent", "fieldtype": "Percent", "width": 120, "precision": 2},
        ]

def get_data(filters):
    """Retrieve book data based on filters"""
    conditions = get_conditions(filters)
    
    if filters.get("show_individual_books"):
        # Query for individual books
        data = frappe.db.sql(f"""
            SELECT 
                b.name as book_code,
                b.book_title,
                b.status,
                b.location,
                b.shelf,
                b.condition
            FROM `tabBook` b
            WHERE b.docstatus = 0 {conditions}
            ORDER BY b.book_title, b.name
        """, filters, as_dict=True)
    else:
        # Query for grouped summary
        data = frappe.db.sql(f"""
            SELECT 
                b.book_title,
                COUNT(b.name) as total,
                SUM(CASE WHEN b.status = 'Available' THEN 1 ELSE 0 END) as available,
                SUM(CASE WHEN b.status = 'Issued' THEN 1 ELSE 0 END) as borrowed,
                SUM(CASE WHEN b.status IN ('Lost', 'Damaged') THEN 1 ELSE 0 END) as lost_damaged,
                ROUND(SUM(CASE WHEN b.status = 'Available' THEN 1 ELSE 0 END) * 100.0 / 
                    NULLIF(COUNT(b.name), 0), 2) as availability_percent
            FROM `tabBook` b
            WHERE b.docstatus = 0 {conditions}
            GROUP BY b.book_title
            ORDER BY b.book_title
        """, filters, as_dict=True)
    
    return data

def get_conditions(filters):
    """Build SQL conditions based on filters"""
    conditions = []
    
    if filters.get("book_title"):
        conditions.append("AND b.book_title = %(book_title)s")
    if filters.get("status"):
        conditions.append("AND b.status = %(status)s")
    if filters.get("location"):
        conditions.append("AND b.location = %(location)s")
    if filters.get("from_date"):
        conditions.append("AND b.purchase_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("AND b.purchase_date <= %(to_date)s")
    
    return " ".join(conditions) if conditions else ""

def add_summary_row(data):
    """Add a summary row at the end with totals"""
    if not data:
        return data
    
    total_row = {
        "book_title": "<b>Total</b>",
        "total": sum(d.get("total", 0) for d in data),
        "available": sum(d.get("available", 0) for d in data),
        "borrowed": sum(d.get("borrowed", 0) for d in data),
        "lost_damaged": sum(d.get("lost_damaged", 0) for d in data),
        "availability_percent": round(
            sum(d.get("available", 0) for d in data) * 100.0 / 
            max(1, sum(d.get("total", 0) for d in data)), 
            2
        ),
        "indent": 0,
        "is_summary": True
    }
    
    data.append(total_row)
    return data

def get_filters():
    """Return filter fields for the report"""
    return [
        {
            "fieldname": "show_individual_books",
            "label": _("Show Individual Books"),
            "fieldtype": "Check",
            "default": 0
        },
        {
            "fieldname": "book_title",
            "label": _("Book Title"),
            "fieldtype": "Link",
            "options": "Book Title"
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Select",
            "options": "\nAvailable\nIssued\nLost\nDamaged"
        },
        {
            "fieldname": "location",
            "label": _("Location"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "from_date",
            "label": _("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": _("To Date"),
            "fieldtype": "Date"
        }
    ]