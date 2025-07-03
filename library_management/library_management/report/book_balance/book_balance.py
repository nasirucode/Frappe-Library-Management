import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    
    columns = get_columns(filters)
    data = get_data(filters)
    
    if not filters.get("show_individual_books") and not filters.get("name"):
        data = add_summary_row(data)
    
    return columns, data

def get_columns(filters):
    if filters.get("show_individual_books"):
        return [
            {"label": _("Book Code"), "fieldname": "name", "fieldtype": "Link", "options": "Book", "width": 120},
            {"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Link", "options": "Book Title", "width": 200},
            {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
            {"label": _("Location"), "fieldname": "location", "fieldtype": "Data", "width": 150},
        ]
    else:
        return [
            {"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Link", "options": "Book Title", "width": 300},
            {"label": _("Total Copies"), "fieldname": "total", "fieldtype": "Int", "width": 120},
            {"label": _("Available Copies"), "fieldname": "available", "fieldtype": "Int", "width": 140},
            {"label": _("Issued Copies"), "fieldname": "issued", "fieldtype": "Int", "width": 130},
            {"label": _("Lost/Damaged"), "fieldname": "lost_damaged", "fieldtype": "Int", "width": 140},
            {"label": _("Available %"), "fieldname": "availability", "fieldtype": "Percent", "width": 100, "precision": 1},
        ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    if filters.get("show_individual_books"):
        query = """
            SELECT 
                b.name,
                b.book_title,
                b.status,
                b.location
            FROM `tabBook` b
            WHERE b.docstatus = 0 {conditions}
            ORDER BY b.book_title, b.name
        """.format(conditions=conditions)
    else:
        query = """
            SELECT 
                b.book_title,
                COUNT(b.name) as total,
                SUM(IF(b.status='Available', 1, 0)) as available,
                SUM(IF(b.status='Issued', 1, 0)) as issued,
                SUM(IF(b.status IN ('Lost', 'Damaged'), 1, 0)) as lost_damaged,
                ROUND(SUM(IF(b.status='Available', 1, 0)) * 100.0 / 
                GREATEST(COUNT(b.name), 1), 1) as availability
            FROM `tabBook` b
            WHERE b.docstatus = 0 {conditions}
            GROUP BY b.book_title
            ORDER BY b.book_title
        """.format(conditions=conditions)
    
    return frappe.db.sql(query, filters, as_dict=True)

def get_conditions(filters):
    conditions = []
    
    if filters.get("book_title"):
        conditions.append("AND b.book_title = %(book_title)s")
    if filters.get("status"):
        conditions.append("AND b.status = %(status)s")
    if filters.get("location"):
        conditions.append("AND b.location = %(location)s")
    if filters.get("name"):
        conditions.append("AND b.name = %(name)s")
    
    return " ".join(conditions)

def add_summary_row(data):
    if not data:
        return data
    
    total = sum(d.get("total", 0) for d in data)
    available = sum(d.get("available", 0) for d in data)
    issued = sum(d.get("issued", 0) for d in data)
    lost_damaged = sum(d.get("lost_damaged", 0) for d in data)

    availability = round(available * 100.0 / max(total, 1), 1)

    data.append({
        "book_title": "Total",
        "total": total,
        "available": available,
        "issued": issued,
        "lost_damaged": lost_damaged,
        "availability": availability,
        "indent": 0,
        "bold": 1,
        "is_total_row": True
    })

    return data

# Optional, but helpful for JS side to load dynamically (if needed via JS Report)
def get_report_filters():
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
        }
    ]
