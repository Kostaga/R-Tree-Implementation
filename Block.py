from record import Record
from bounding_area import BoundingArea
from copy import deepcopy
import variables

class Block:
	max: int = (variables.BLOCKSIZE // variables.RECORDSIZE)
	min: int = variables.M * max
	
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


	
	def calculate_overlap_area(self, mbr):
		"""
		:param mbr: MBR object to calculate the overlap area
		:return: Overlap area
		"""
		# Initialize the overlap area
		overlap_area = 0
		# Iterate over the elements in the block
		for element in self.elements:
			# Calculate the overlap area
			if element != mbr:
				overlap_area += mbr.area_overlap(element)
		# Return the overlap area
		return overlap_area


	def calculate_overlap_enlargement(self, mbr: BoundingArea, record: Record):
		copy_mbr = deepcopy(mbr)
		copy_mbr.add_point(record)
		overlap_enlargement = self.calculate_overlap_area(copy_mbr) - self.calculate_overlap_area(mbr) - copy_mbr.overlap_area(mbr)
		return overlap_enlargement
		
		


	def calculate_least_overlap_enlargement(self, record: Record):
		least_overlap_enlargement = float('inf')
		area_enlargement = float('inf')
		for element in self.elements:
			overlap_enlargement = self.calculate_overlap_enlargement(element, record)
			if overlap_enlargement < least_overlap_enlargement or (overlap_enlargement == least_overlap_enlargement and element.calculate_area_enlargement(record) < area_enlargement):
				least_overlap_enlargement = overlap_enlargement
				area_enlargement = element.calculate_area_enlargement(record)
		return least_overlap_enlargement
	

		

	# Return the number of elements in the block
	def __len__(self) -> int:
		return len(self.elements)
	

	def __str__(self):
		return f"Block {self.blockID}: {len(self.elements)} elements"
