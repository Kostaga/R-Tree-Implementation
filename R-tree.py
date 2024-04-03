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
		node = self.root
		
		while (not node.isLeaf):
			 # If the child pointers point to leaves, 
			# determine minimum overlap cost
			if (levelToAdd == 1): # If at level 1, just use minimum overlap cost
				minCost = self.minOverlap(node,block)

			else:
				# Otherwise, use minimum area cost selection
				minCost = self.minArea(node,block)
			
			# Choose the child node based on the minimum cost
			
			# Don't know yet how to implement this
			
			# Adjust level accordingly
			levelToAdd -= 1


		return node
		


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
