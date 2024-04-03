from Record import Record
import Variables
class Block:
	# Intialize Block object, with blockID and empty records list
	def __init__(self, blockID: int, isLeaf: bool, levels: int):
		self.blockID: int = blockID
		self.records: list[Record] = [] # List of records
		self.min: int = Variables.M
		self.max: int = (Variables.BLOCKSIZE // Variables.RECORDSIZE)
		self.isLeaf: bool = isLeaf
		self.levels: int = levels
		self.child_pointers: list[Block] = [] # List of child pointers


	# Insert a record to the block
	def insertRecord(self, record: Record) -> None:
		"""""
		:param record: Record object to insert
		:return: None
		"""
		# Check if the block is full
		if len(self.records) < self.max:
			# Insert the record to the block
			self.records.append(record)
		else:
			raise ValueError("Block is full")
		
	
	# Check if the block is full
	def is_full(self) -> bool:
		"""
		:return: True if the block is full, False otherwise
		"""
		return len(self.records) == self.max

		

	# Return the number of records in the block
	def __len__(self) -> int:
		return len(self.records)
	

	def __str__(self):
		return f"Block {self.blockID}: {len(self.records)} records"
