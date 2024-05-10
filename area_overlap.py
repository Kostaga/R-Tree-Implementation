from block import Block
from record import Record
from bounding_area import BoundingArea
from copy import deepcopy


def calculate_overlap_area(block: Block, mbr: BoundingArea):
	"""
	:param mbr: MBR object to calculate the overlap area with the rest of the elements in the block
	:return: Overlap area
	"""
	if block.is_leaf:
		raise ValueError("Block is a leaf")  # block must be a non-leaf
      
	# Initialize the overlap area
	overlap_area = 0
	# Iterate over the elements in the block
	for element in block.elements:
		# Calculate the overlap area
		if element != mbr:
			overlap_area += mbr.area_overlap(element)
	# Return the overlap area
	return overlap_area


def calculate_overlap_enlargement(block: Block, mbr: BoundingArea, record: Record):
	"""
	:param mbr: MBR object to calculate the overlap enlargement with the rest of the elements in the block
	:param record: Record object to be inserted to the mbr
	:param block: Block object that includes the mbr
	:return: Overlap enlargement
	"""
	if block.is_leaf:
		raise ValueError("Block is a leaf")  # block must be a non-leaf
    
	copy_mbr: BoundingArea = deepcopy(mbr)
	copy_mbr.include_point(record)
	overlap_enlargement = calculate_overlap_area(block, copy_mbr) - calculate_overlap_area(block, mbr) - copy_mbr.area_overlap(mbr)  # minus the copy.overlap_area(mbr) to avoid double counting --> it works!!!
	return overlap_enlargement
    

def calculate_least_overlap_enlargement(block: Block, record: Record):
	'''
	:param block: Block object that includes mbr elements
	:param record: Record object to be included to the mbrs
	:return: index of the mbr with the least overlap enlargement if the record is to be included in that mbr
	'''
	if block.is_leaf:
		raise ValueError("Block is a leaf")  # block must be a non-leaf
    
	least_overlap_enlargement = float('inf')
	chosen_area_enlargement = float('inf')
	mbr_index = -1  # index of mbr with least overlap enlargement
	mbr: BoundingArea = None  # mbr with least overlap enlargement -- to type hint mbr in the for-loop (better for readability)

	for i, mbr in enumerate(block.elements):  # mbr is BoundingArea object
		overlap_enlargement = calculate_overlap_enlargement(block, mbr, record)
		if overlap_enlargement < least_overlap_enlargement or (overlap_enlargement == least_overlap_enlargement and mbr.calculate_area_enlargement(record) < chosen_area_enlargement):
			# new best mbr
			least_overlap_enlargement = overlap_enlargement
			chosen_area_enlargement = mbr.calculate_area_enlargement(record)
			mbr_index = i  # this is the juice
	return mbr_index