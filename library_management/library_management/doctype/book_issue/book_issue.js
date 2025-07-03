// Copyright (c) 2025, Isyaku Murtala and contributors
// For license information, please see license.txt
// Book Issue (Parent Doctype)
frappe.ui.form.on('Book Issue', {
    before_save: function (frm) {
        if (!frm.doc.issue_date) {
            frm.set_value('issue_date', frappe.datetime.now_datetime());
        }

        if (!frm.doc.librarian) {
            frm.set_value('librarian', frappe.session.user);
        }
    },

    onload: function (frm) {
        frm.set_df_property('issue_date', 'read_only', 1);
        frm.set_df_property('librarian', 'read_only', 1);
    }
});

// Book Issue Item (Child Table)
frappe.ui.form.on('Book Issue Item', {
    // Auto-fetch book_code from selected book
    book: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.book) {
            frappe.model.get_value('Book', row.book, 'book_code', (r) => {
                if (r && r.book_code) {
                    frappe.model.set_value(cdt, cdn, 'book_code', r.book_code);
                }
            });
        }
    },

    // Filter available books on row add
    books_issued_add: function (frm, cdt, cdn) {
        frm.fields_dict["books_issued"].grid.get_field("book").get_query = function () {
            return {
                filters: {
                    status: "Available"
                }
            };
        };
    }
});
