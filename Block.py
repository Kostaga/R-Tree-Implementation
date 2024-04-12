from Record import Record
import Variables
class Block:
	max: int = (Variables.BLOCKSIZE: int // Variables.RECORDSIZE:int )
	min: int = Variables.M * max
	
	# Intialize Block object, with blockID and empty elements list
	def __init__(self, isLeaf: bool, levels: int):
		# self.blockID: int = blockID
		self.elements: list = [] # List of MBRs/elements # Percentage of M
		self.isLeaf: bool = isLeaf
		self.levels: int = levels

	# Insert a record to the block
	def insert(self, record: Record) -> None:
		"""""
		:param record: Record object to insert
		:return: None
		"""
		# Check if the block is full
		if len(self.elements) < Block.max:
			# Insert the record toBlock block
			self.elements.append(record)
		else:
			raise ValueError("Block is full")
		
	
	# Check if the block is full
	def is_full(self) -> bool:
		"""
		:return: True if the block is full, False otherwise
		"""
		return len(self.elements) == self.max

		

	# Return the number of elements in the block
	def __len__(self) -> int:
		return len(self.elements)
	

	def __str__(self):
		return f"Block {self.blockID}: {len(self.elements)} elements"
