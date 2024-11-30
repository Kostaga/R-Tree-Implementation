from record import Record
import variables

class Block:
	max: int = (variables.BLOCKSIZE // variables.RECORDSIZE)
	min: int = int(variables.M * max)
	
	# Intialize Block object, with blockID and empty elements list
	def __init__(self, is_leaf: bool, parent_mbr, parent_block):  # parent_mbr is the boundingArea that points to this block of elements
		self.elements: list = [] # List of MBRs/elements # Percentage of M
		self.is_leaf: bool = is_leaf
		self.parent_mbr = parent_mbr  # mbr that has a pointer next_block to this block
		self.parent_block = parent_block 


	def get_level(self):
		level = 0
		current_block = self
		while(current_block.parent_block != None):  # root has no parent_mbr - so root has level 0
			current_block = current_block.parent_block
			level += 1
		return level

	# Insert a record to the block
	def insert(self, record: Record):
		"""""
		:param record: Record object to insert
		:return: None
		"""
		# Check if the block is full
		if not self.is_full():
			# Insert record to block
			self.elements.append(record)
		else:
			self.elements.append(record)
			# block gets overflowed so the split functions work properly and an exception is raised that is to 
			# be dealt with elsewhere with try: ... except OverflowError: ...
			raise OverflowError("Block is full")


	def delete(self, element):  # element may be a record or a boundingArea - it doesn't matter
		"""
		:param record: Element to delete
		:return: None
		"""
		try:
			self.elements.remove(element)
			return True
		except ValueError:  # element does not exist in the block - for debugging
			return False
		
		
	
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
		final_str = ""
		if self.is_leaf:
			final_str += "Leaf Block\n"
		else:
			final_str += "Non-Leaf Block\n"
		for element in self.elements:
			final_str += str(element) + "\n"
		return final_str
