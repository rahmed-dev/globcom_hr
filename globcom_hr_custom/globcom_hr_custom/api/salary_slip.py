import frappe


def set_overtime_hours(doc, method=None):
	"""
	Fetch and sum overtime hours from Overtime Entry records for the employee.

	Args:
		doc: Salary Slip document
		method: Hook method (optional)

	Logic:
		1. Get employee, start_date, end_date from Salary Slip
		2. Query Overtime Entry where:
		   - payroll_date BETWEEN start_date AND end_date
		   - docstatus = 1 (submitted)
		3. For each matching Overtime Entry, get child table records where employee matches
		4. Sum all overtime_hrs values
		5. Set doc.custom_overtime_hrs = total
	"""
	if not doc.employee or not doc.start_date or not doc.end_date:
		return

	# Query to sum overtime hours from Overtime Entry Details
	# Join parent Overtime Entry to filter by payroll_date and docstatus
	total_overtime_hrs = frappe.db.sql("""
		SELECT IFNULL(SUM(detail.overtime_hrs), 0) as total_overtime
		FROM `tabOvertime Entry Detail` detail
		INNER JOIN `tabOvertime Entry` parent
			ON detail.parent = parent.name
		WHERE parent.payroll_date BETWEEN %(start_date)s AND %(end_date)s
			AND parent.docstatus = 1
			AND detail.employee = %(employee)s
	""", {
		"start_date": doc.start_date,
		"end_date": doc.end_date,
		"employee": doc.employee
	}, as_dict=True)

	# Set the overtime hours in the custom field
	if total_overtime_hrs:
		doc.custom_overtime_hrs = total_overtime_hrs[0].get("total_overtime", 0.0)
	else:
		doc.custom_overtime_hrs = 0.0
