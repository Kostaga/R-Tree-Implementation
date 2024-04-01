from Record import Record

class Block:
	# Intialize Block object, with blockID and empty records list
	def __init__(self, blockID: int):
		self.blockID = blockID
		self.records = []
	

	# Insert a record to the block
	def insert(self, record: Record):
		"""""
		:param record: Record object to insert
		:return: None
		"""
		self.records.append(record)


	# Return the number of records in the block
	def __len__(self) -> int:
		return len(self.records)
	

	def __str__(self):
		return f"Block {self.blockID}: {len(self.records)} records"
