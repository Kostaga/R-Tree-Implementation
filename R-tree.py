from Record import Record
from Block import Block
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
			self.root = Block(blockID=0, isLeaf=True, levels=1)
			self.root.insertRecord(record)
			return
		
		#I1 Invoke ChooseSubtree. with the level as a parameter,
		# to find an appropriate node N, m which to place the
		# new entry E
		subtree = self.chooseSubtree(self.root,self.root.levels)
		overflowFlag = False


		if (subtree.__len__() < subtree.max):
			 # If N has less than M entries, accommodate E in N
			subtree.insertRecord(record)
			
		else:
			# If N has M entries, invoke OverflowTreatment
			overflowFlag = True
			self.overflowTreatment(subtree,subtree.levels,record)
			

	def chooseSubtree(self, block: Block, levelToAdd: int,) -> Block:
		"""
        Choose the subtree to insert a new record based on 
		minimum overlap or area cost.
        """

		#CSl Set N to be the root
		node = self.root
		#CS2 If N 1s a leaf, return N 
		if (node.isLeaf):
			return node
		
		# else
		# if the childpointers in N point to leaves, determine minimum overlap cost
		if all(child.isLeaf for child in node.childPointers):
			# Determine minimum overlap cost
			min_overlap_cost = float('inf')
			min_area_enlargement = float('inf')
			min_area = float('inf')
			chosen_entry = None

			for entry in node.records:
				overlap_cost = entry.rectangle.calculateOverlapCost(record.rectangle)
				if overlap_cost < min_overlap_cost:
					min_overlap_cost = overlap_cost
					min_area_enlargement = entry.rectangle.calculateAreaEnlargement(record.rectangle)
					min_area = entry.rectangle.calculateArea()
					chosen_entry = entry
				elif overlap_cost == min_overlap_cost:
					area_enlargement = entry.rectangle.calculateAreaEnlargement(record.rectangle)
					if area_enlargement < min_area_enlargement:
						min_area_enlargement = area_enlargement
						min_area = entry.rectangle.calculateArea()
						chosen_entry = entry
					elif area_enlargement == min_area_enlargement:
						area = entry.rectangle.calculateArea()
						if area < min_area:
							min_area = area
							chosen_entry = entry

			return chosen_entry.childPointer
		

		


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


	def rangeQuery(self, corners: list) -> list:
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
