from record import Record 

def z_order_curve(records: list[Record]) -> list[Record]:
	"""
	:param records: A list of point coords
	:return: List of records sorted by Z-order curve
	"""
	def calculate_z_order(coords: tuple) -> int:
		"""Helper function to calculate Z-order for a point in any number of dimensions."""
		z = 0
		coords = [round(coord) for coord in coords]
		max_bits = max(coord.bit_length() for coord in coords)
		for i in range(max_bits):
			for j, coord in enumerate(coords):
				z |= ((coord >> i) & 1) << (i * len(coords) + j)
		return z

    # Assuming each record has an attribute `coords` which is a list of its coordinates.
	for record in records:
		record.z_value = calculate_z_order(record.location)

    # Sort records by their Z-order value.
	sorted_records = sorted(records, key=lambda record: record.z_value)
	    
	return sorted_records
