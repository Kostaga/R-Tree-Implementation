from record import Record
from block import Block
from bounding_area import BoundingArea
import variables


class RTree():
	
	def __init__(self):
		self.blocks = []
		self.root = None
	

	def insert(self, record: Record):
		"""
		:param record: Record object to insert
		:return: None
		"""
		if (self.root == None):
			self.root = Block(isLeaf=True, levels=1)
			self.root.insert(record)
			return
	
		re_insert_flag: bool = False
		
		# I1 Invoke ChooseSubtree. with the level as a parameter,
		# to find an appropriate node N, m which to place the
		# new entry E
		leaf: Block = self.chooseSubtree(record)
		

		if not leaf.is_full():
			# If N has less than M entries, accommodate E in N
			leaf.insert(record)
			
		else:
			# If N has M entries, invoke OverflowTreatment
			re_insert_flag = self.overflowTreatment(leaf.levels)

			if (re_insert_flag): # If boolean variable is true, invoke reinsert
				self.reInsert(leaf,record)
			
			else: # else, split the node
				returned_block = self.splitNode(leaf,record)
				
				if (returned_block is not None):
					# If a new block was returned, create a new root
					self.root = returned_block
					self.root.levels = self.root.elements[0].next_block.levels + 1
				
			
	

	def reInsert(self, block: Block, record: Record):
		"""
		Reinsert the elements in the block.
		"""

		# percentage of M to be reinserted
		p = round(variables.P * variables.M)
		
		# RI1 Compute the distance between the centers of their rectangles
		# and the center of the bounding rectangle of N
		pairs = []
		for element in block.elements:
			# Calculate the center distance (yet to be implemented)
			distance = element.calculate_center_distance(record)
			pairs.append((element, distance))
		
		# RI2 Sort the entries in decreasing order of their distances
		pairs.sort(key=lambda x: x[1], reverse=True)

		# RI3 Remove the first p entries from N and adjust the bounding rectangle
		# of N
		pairs = pairs[:p]

		
		# RI4 in the sort defined in RI2, starting with the maximum distance
		# or minimum distance, invoke insert to reinsert the entries
  
			
		# not yet implemented





	def chooseSubtree(self, record: Record) -> Block:
		"""
        Choose the subtree to insert a new record based on 
		minimum overlap or area cost.
        """
		#CS1 Let N be the root
		current_node: Block = self.root
		#CS2 If N 1s a leaf, return N 
		if (current_node.isLeaf):
			return current_node
		
		# else
		# if the childpointers in N point to leaves, determine minimum overlap cost
		
		# Determine minimum overlap cost
		while not current_node.elements[0].next_block.isLeaf:
			# CS3 Choose the entry E from N that needs least area enlargement to include R
			min_area_enlargement = float('inf')
			best_mbr = None
			for mbr in current_node.elements:
				area_enlargement = mbr.calculate_area_enlargement(record)
				if area_enlargement < min_area_enlargement or (area_enlargement == min_area_enlargement and best_mbr.area > mbr.area):
					min_area_enlargement = area_enlargement
					best_mbr = mbr
			
			current_node = best_mbr.next_block

		# Current node has child pointers that point to leaves
		# Determine minimum area enlargement
		
		best_mbr = current_node.calculate_least_overlap_enlargement(record)
		chosen_leaf = best_mbr.next_block

		return chosen_leaf



	
	def overflowTreatment(self, block: Block, level: int) -> bool:
		# OTl If the level 1s not the root level and this IS the first
		# call of OverflowTreatment m the given level
		# durmg the Insertion of one data rectangle, then
		if level != 1:
			# Mark level as already inserted
			if (block.levels not in block.level_overflow):
				block.level_overflow.add(level)
				return True

		return False
	
	

	def splitNode(self, block: Block, record: Record):
		"""
		Split the node when it overflows.
		"""
		pass

		 
			
	def delete(self, record: Record):
		"""
		:param record: Record object to delete
		:return: None
		"""
		pass


	def search(self, record: Record):
		"""
		:param record: Record object to delete
		:return: None
		"""
		pass


	def rangeQuery(self, area: BoundingArea) -> list:
		"""
		:param corners: A list of (d-1)-dimensional rectangle's corners
		:return: List of records included in the range query

		2d: corners = [(x1, y1), (x2, y2)]
		3d: corners = [(x1, y1, z1), (x2, y2, z2)]
		"""
		pass

	def nearestNeighbor(self, point: list, k: int) -> Record:
		"""
		:param record: A list of points
		:return: k Records which are the nearest neighbor to the given point
		"""
		pass


	def bottomUp(self, points: list):
		"""
		:param records: A list of point coords
		:return: None
		"""
		pass
