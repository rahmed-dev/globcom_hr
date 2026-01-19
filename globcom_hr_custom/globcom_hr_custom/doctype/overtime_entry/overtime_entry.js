// Copyright (c) 2026, Globcom and contributors
// For license information, please see license.txt

frappe.ui.form.on("Overtime Entry", {
	fetch_employees(frm) {
		// Validate required fields
		if (!frm.doc.company) {
			frappe.msgprint(__("Please select a Company first"));
			return;
		}

		// Call server-side method to fetch employees
		frappe.call({
			method: "globcom_hr_custom.globcom_hr_custom.doctype.overtime_entry.overtime_entry.fetch_employees_for_overtime",
			args: {
				company: frm.doc.company,
				shift: frm.doc.shift || null,
				department: frm.doc.department || null,
				designation: frm.doc.designation || null
			},
			callback: function(r) {
				if (r.message && r.message.length > 0) {
					// Get existing employee IDs to avoid duplicates
					let existing_employees = frm.doc.overtime_entry_details.map(row => row.employee);

					let added_count = 0;
					r.message.forEach(employee => {
						// Only add if employee doesn't already exist in child table
						if (!existing_employees.includes(employee.name)) {
							let row = frm.add_child("overtime_entry_details");
							row.employee = employee.name;
							added_count++;
						}
					});

					frm.refresh_field("overtime_entry_details");

					if (added_count > 0) {
						frappe.show_alert({
							message: __("{0} employee(s) added", [added_count]),
							indicator: "green"
						});
					} else {
						frappe.show_alert({
							message: __("All matching employees are already in the list"),
							indicator: "blue"
						});
					}
				} else {
					frappe.msgprint(__("No active employees found matching the filters"));
				}
			}
		});
	}
});
