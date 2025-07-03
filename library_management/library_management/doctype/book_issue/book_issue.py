# Copyright (c) 2025, Isyaku Murtala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


def update_book_status(book_code, status):
    frappe.db.set_value("Book", book_code, "status", status)

def set_books_as_issued(doc):
    for item in doc.books_issued:
        update_book_status(item.book, "Issued")

def set_books_as_available(doc):
    for item in doc.books_issued:
        update_book_status(item.book, "Available")

def on_submit(doc, method):
    set_books_as_issued(doc)

def on_cancel(doc, method):
    set_books_as_available(doc)


class BookIssue(Document):
    def before_save(self):
        # Set issue date if not already set
        if not self.issue_date:
            self.issue_date = now_datetime()

 		# Set librarian to current logged-in user if not already set
        if not self.librarian:
            self.librarian = frappe.session.user