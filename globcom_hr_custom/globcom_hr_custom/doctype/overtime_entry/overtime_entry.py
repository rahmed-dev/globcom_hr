# Copyright (c) 2026, Globcom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OvertimeEntry(Document):
	pass


@frappe.whitelist()
def fetch_employees_for_overtime(company, shift=None, department=None, designation=None):
	"""
	Fetch active employees based on filter criteria.

	Args:
		company: Company name (required)
		shift: Shift Type (optional) - checks both default_shift and Shift Assignment
		department: Department (optional)
		designation: Designation (optional)

	Returns:
		List of employee dicts with name and employee_name
	"""
	if not company:
		frappe.throw("Company is required to fetch employees")

	# If shift filter is provided, use SQL query to check both default_shift and Shift Assignment
	if shift:
		query = """
			SELECT DISTINCT e.name, e.employee_name
			FROM `tabEmployee` e
			WHERE e.status = 'Active'
				AND e.company = %(company)s
				AND (
					e.default_shift = %(shift)s
					OR EXISTS (
						SELECT 1 FROM `tabShift Assignment` sa
						WHERE sa.employee = e.name
							AND sa.shift_type = %(shift)s
							AND sa.docstatus = 1
					)
				)
				{department_filter}
				{designation_filter}
			ORDER BY e.employee_name
		"""

		# Build dynamic filters
		department_filter = "AND e.department = %(department)s" if department else ""
		designation_filter = "AND e.designation = %(designation)s" if designation else ""

		query = query.format(
			department_filter=department_filter,
			designation_filter=designation_filter
		)

		employees = frappe.db.sql(query, {
			"company": company,
			"shift": shift,
			"department": department,
			"designation": designation
		}, as_dict=True)
	else:
		# No shift filter - use simple frappe.get_all
		filters = {
			"status": "Active",
			"company": company
		}

		if department:
			filters["department"] = department
		if designation:
			filters["designation"] = designation

		employees = frappe.get_all(
			"Employee",
			filters=filters,
			fields=["name", "employee_name"],
			order_by="employee_name"
		)

	return employees
