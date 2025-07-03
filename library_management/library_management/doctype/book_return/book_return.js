// Copyright (c) 2025, Isyaku Murtala and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Book Return", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Book Return', {
    before_save: function (frm) {
        if (!frm.doc.issue_date) {
            frm.set_value('return_date', frappe.datetime.now_datetime());
        }

        if (!frm.doc.librarian) {
            frm.set_value('librarian', frappe.session.user);
        }
    },

    onload: function (frm) {
        frm.set_df_property('return_date', 'read_only', 1);
        frm.set_df_property('librarian', 'read_only', 1);
    },

    student: function (frm) {
        if (!frm.doc.student) return;

        frappe.call({
            method: 'library_management.library_management.doctype.book_return.book_return.get_unreturned_books',
            args: {
                student: frm.doc.student
            },
            callback: function (r) {
                console.log("Books returned from server:", r.message); // ✅ Add this
                if (r.message) {
                    frm.clear_table("books_returned");

                    r.message.forEach(function (book) {
                        let row = frm.add_child("books_returned");
                        row.book = book.book;
                        row.book_title = book.book_title;
                        row.book_code = book.book_code;
                        row.issue_item = book.issue_item;
                    });

                    frm.refresh_field("books_returned");
                }
            }
        });

    }
});


// frappe.ui.form.on('Book Return Item', {
//     // Auto-fetch book_code from selected book
//     book: function (frm, cdt, cdn) {
//         let row = locals[cdt][cdn];
//         if (row.book) {
//             frappe.model.get_value('Book', row.book, 'book_code', (r) => {
//                 if (r && r.book_code) {
//                     frappe.model.set_value(cdt, cdn, 'book_code', r.book_code);
//                 }
//             });
//         }
//     },
// });
