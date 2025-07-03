# Copyright (c) 2025, Isyaku Murtala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookReturn(Document):
	pass

    
        
# def on_submit(doc, method):
#     for item in doc.books_returned:
#         if item.issue_item:
#             frappe.db.set_value("Book Issue Item", item.issue_item, "returned", 1)
#         frappe.db.set_value("Book", item.book, "status", "Available")

@frappe.whitelist()
def on_submit(doc, method):
    for item in doc.books_returned:
        if item.book:
            status = "Available"  # default

            if item.condition == "Damaged":
                status = "Damaged"
            elif item.condition == "Lost":
                status = "Lost"

            frappe.db.set_value("Book", item.book, "status", status)

        # Also mark the issue item as returned
        if item.issue_item:
            frappe.db.set_value("Book Issue Item", item.issue_item, "returned", 1)




@frappe.whitelist()
def get_unreturned_books(student):
    return frappe.db.sql("""
        SELECT
            bii.book,
            b.title AS book_title,
            b.book_code,
            bii.name AS issue_item
        FROM
            `tabBook Issue Item` bii
        JOIN
            `tabBook Issue` bi ON bii.parent = bi.name
        JOIN
            `tabBook` b ON b.name = bii.book
        WHERE
            bi.student = %s AND
            bii.returned = 0 AND
            bi.docstatus = 1
    """, (student,), as_dict=True)



    return issued_items

