import frappe


def calculate_total_earning(doc, method=None):
	"""
	Calculate total earning from custom allowance fields in Salary Structure Assignment.

	Args:
		doc: Salary Structure Assignment document
		method: Hook method (optional)

	Logic:
		Sum all custom allowance fields:
		- custom_hra_amount
		- custom_ta_amount
		- custom_mobile_allowance_amount
		- custom_food_allowance_amount
		- custom_other_allowance_amount

		Set the total to doc.custom_total_earning
	"""
	total_earning = 0.0

	# Sum all earning components
	earning_fields = [
		'base',
		'custom_hra_amount',
		'custom_ta_amount',
		'custom_mobile_allowance_amount',
		'custom_food_allowance_amount',
		'custom_other_allowance_amount'
	]

	for field in earning_fields:
		amount = doc.get(field) or 0.0
		total_earning += amount

	# Set the calculated total
	doc.custom_total_earning = total_earning
