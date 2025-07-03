// Copyright (c) 2025, Isyaku Murtala and contributors
// For license information, please see license.txt

frappe.query_reports["Book Balance"] = {
	"filters": [

	]
};
frappe.query_reports["Book Balance"] = {
    filters: [
        {
            fieldname: "show_individual_books",
            label: "Show Individual Books",
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "book_title",
            label: "Book Title",
            fieldtype: "Link",
            options: "Book Title"
        },
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nAvailable\nIssued\nLost\nDamaged"
        },
        {
            fieldname: "location",
            label: "Location",
            fieldtype: "Data"
        }
    ],

    onload: function (report) {
        report.page.add_inner_button("View Books for Title", () => {
            const bookTitle = report.get_filter_value("book_title");
            if (!bookTitle) {
                frappe.msgprint("Please select a Book Title first.");
                return;
            }

            frappe.set_route("query-report", "Book Balance", {
                book_title: bookTitle,
                show_individual_books: 1
            });
        }, "Actions");
    }
};
