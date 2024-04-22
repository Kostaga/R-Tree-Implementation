from block import Block
from record import Record
from bounding_area import BoundingArea
from copy import deepcopy


def calculate_overlap_area(block: Block, mbr: BoundingArea):
		"""
		:param mbr: MBR object to calculate the overlap area
		:return: Overlap area
		"""
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
    copy_mbr = deepcopy(mbr)
    copy_mbr.add_point(record)
    overlap_enlargement = block.calculate_overlap_area(copy_mbr) - block.calculate_overlap_area(mbr) - copy_mbr.overlap_area(mbr)
    return overlap_enlargement
    

def calculate_least_overlap_enlargement(block: Block, record: Record):
    least_overlap_enlargement = float('inf')
    area_enlargement = float('inf')
    for element in block.elements:  # element is BoundingArea object
        overlap_enlargement = block.calculate_overlap_enlargement(element, record)
        if overlap_enlargement < least_overlap_enlargement or (overlap_enlargement == least_overlap_enlargement and element.calculate_area_enlargement(record) < area_enlargement):
            least_overlap_enlargement = overlap_enlargement
            area_enlargement = element.calculate_area_enlargement(record)
    return least_overlap_enlargement