from Record import Record
from Block import Block
from Bounding_area import BoundingArea


class RTree():

	def __init__(self):
		self.blocks = []
		self.root = None
		self.levels = [True for i in levels]
	

	def insert(self, record: Record):
		"""
		:param record: Record object to insert
		:return: None
		"""
		if (self.root == None):
			self.root = Block(isLeaf=True, levels=1)
			self.root.insert(record)
			return
		
		# I1 Invoke ChooseSubtree. with the level as a parameter,
		# to find an appropriate node N, m which to place the
		# new entry E
		leaf: Block = self.chooseSubtree(record)
		overflowFlag = False


		if not leaf.is_full():
			# If N has less than M entries, accommodate E in N
			leaf.insert(record)
			
		else:
			# If N has M entries, invoke OverflowTreatment
			overflowFlag = True
			self.overflowTreatment(leaf,leaf.levels,record)
			

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
				if area_enlargement < min_area_enlargement:
					min_area_enlargement = area_enlargement
					best_mbr = mbr
			
			current_node = best_mbr.next_block

		# Current node has child pointers that point to leaves
		# Determine minimum area enlargement
		# min_overlap_cost = float('inf')
		# PASS

		return current_node
				
	
	def overflowTreatment(self,level: int):
		# OTl If the level 1s not the root level and this IS the first
		# call of OverflowTreatment m the given level
		# durmg the Insertion of one data rectangle, then
		# invoke Reinsert
  		if level != 1:
			# Reinsert()
			pass
		else:
			# SplitNode()
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
