from record import Record
from copy import deepcopy
import variables

class Block:
	max: int = (variables.BLOCKSIZE // variables.RECORDSIZE)
	min: int = variables.M * max

	level_overflow: set = set() # keep track of levels that have been overflowed
	
	# Intialize Block object, with blockID and empty elements list
	def __init__(self, is_leaf: bool, levels: int):
		# self.blockID: int = blockID
		self.elements: list = [] # List of MBRs/elements # Percentage of M
		self.is_leaf: bool = is_leaf
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
		return len(self.elements) == Block.max
		

	# Return the number of elements in the block
	def __len__(self) -> int:
		return len(self.elements)
	

	def __str__(self):
		return f"Block {self.blockID}: {len(self.elements)} elements"
