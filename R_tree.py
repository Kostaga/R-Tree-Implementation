from record import Record
from block import Block
from bounding_area import BoundingArea
import variables
import area_overlap as avp
import split_funcs as sf

import heapq
import kNN_helper as knn


class RTree():
	
	def __init__(self, root=None):  # initialize root only for testing purposes
		self.root = root
	

	def insert(self, record: Record):
		"""
		:param record: Record object to insert
		:return: None
		"""
		if (self.root == None):
			self.root = Block(is_leaf=True, parent_mbr=None)
			self.root.insert(record)
			return
	
		re_insert_flag: bool = False
		
		# I1 Invoke ChooseSubtree. with the level as a parameter,
		# to find an appropriate node N, m which to place the
		# new entry E
		leaf, path = self.chooseSubtree(record)  # index 0 is the chosen leaf - index 1 is the path to the leaf
		

		try:
			# If N has less than M entries, accommodate E in N
			leaf.insert(record)
		except OverflowError:
			# If N has M entries, invoke OverflowTreatment
			re_insert_flag = self.overflowTreatment(leaf.get_level())

			if (re_insert_flag): # If boolean variable is true, invoke reinsert
				self.reInsert(leaf, record)
			
			else: # else, split the node
				new_blocks = self.split_node(leaf, path)  # tuple of the two new blocks

				if (new_blocks is not None):
					# If a new block was returned, create a new root
					self.root = new_blocks
					# self.root.level = self.root.elements[0].next_block.level + 1
				
			
	
	# 1) calculate mbr center
	# 2) calculate distance leaf

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
		# Path of block, MBR that the record will follow to reach the leaf
		path = []

		#CS1 Let N be the root
		current_node: Block = self.root

		#CS2 If N 1s a leaf, return N 
		if (current_node.is_leaf):
			return current_node, path  # path is empty because the leaf is the root

		
		# else
		# if the childpointers in N point to leaves, determine minimum overlap cost
		
		# Determine minimum overlap cost
		# Include point in the passing MBRs ???????
		while not current_node.elements[0].next_block.is_leaf:
			# CS3 Choose the entry E from N that needs least area enlargement to include R
			min_area_enlargement = float('inf')
			best_mbr: BoundingArea = None
			mbr: BoundingArea = None  # type hinting for the for-loop
			for mbr in current_node.elements:
				area_enlargement = mbr.calculate_area_enlargement(record)
				if area_enlargement < min_area_enlargement or (area_enlargement == min_area_enlargement and mbr.area < best_mbr.area):
					min_area_enlargement = area_enlargement
					best_mbr = mbr

			path.append(current_node, best_mbr)			
			current_node = best_mbr.next_block
			

		# Current node has child pointers that point to leaves
		# Determine minimum area enlargement
		
		best_mbr = avp.calculate_least_overlap_enlargement(current_node, record)
		chosen_leaf = best_mbr.next_block
		# Path does not include the leaf

		return chosen_leaf, path


	def overflowTreatment(self, level: int) -> bool:
		# OTl If the level 1s not the root level and this IS the first
		# call of OverflowTreatment m the given level
		# durmg the Insertion of one data rectangle, then
		if level != 0:  # if the level is not the root level --> level 0
			# Mark level as already inserted
			if (level not in Block.level_overflow):
				Block.level_overflow.add(level)
				return True
		return False
	
	
	def split_node(self, node: Block, path: list[tuple[Block, BoundingArea]]) -> None:
		"""
		Split node into two new nodes and insert the new nodes to the parent block.
		:param node: Block to split
		:param path: Path to the node - tuples of (Block, BoundingArea)
		:return: None
		"""

		# Create two new blocks and
		# connect the proper pointers up and down
		if node.is_leaf:  # node is a leaf and hence contains records
			split_axis = sf.choose_split_axis_leaf(node)
			splits = sf.choose_split_index_leaf(split_axis, node)

			new_node1 = Block(is_leaf=True, parent_mbr=None)  # New nodes are leaves
			new_node2 = Block(is_leaf=True, parent_mbr=None)	
			new_mbr1 = BoundingArea(bounds=BoundingArea.find_bounds_of_records(splits[0]), next_block=new_node1)  # next_block is the pointer to leaf1
			new_mbr2 = BoundingArea(bounds=BoundingArea.find_bounds_of_records(splits[1]), next_block=new_node2)  # next_block is the pointer to leaf2
			
		else:  # node is a non-leaf and hence contains bounding areas
			split_axis = sf.choose_split_axis_non_leaf(node)
			splits = sf.choose_split_index_non_leaf(split_axis, node)

			new_node1 = Block(is_leaf=False, parent_mbr=None)  # new nodes are non-leaves
			new_node2 = Block(is_leaf=False, parent_mbr=None)
			new_mbr1 = BoundingArea(bounds=BoundingArea.find_bounds_of_areas(splits[0]), next_block=new_node1)  # next_block is the pointer to leaf1
			new_mbr2 = BoundingArea(bounds=BoundingArea.find_bounds_of_areas(splits[1]), next_block=new_node2)  # next_block is the pointer to leaf2
			
		new_node1.parent_mbr = new_mbr1  # set the parent_mbr of leaf1 to the new mbr1 so wherever the mbr1 goes later in splits, leaf1 will "follow"
		new_node2.parent_mbr = new_mbr2
		new_node1.elements = splits[0]  # allocate the newlly split elements to the new nodes
		new_node2.elements = splits[1]

		if node.parent_mbr == None:  # at root level
			new_root = Block(is_leaf=False, parent_mbr=None)
			new_root.insert(new_mbr1)
			new_root.insert(new_mbr2)
			self.root = new_root
		else:
			# Delete the old mbr from the parent block
			parent_block = path[-1][0]
			old_mbr = path[-1][1]
			# path[-1][1] is the parent mbr that points to the node
			# path[-1][0] is the block that contains the parent mbr
			if not parent_block.delete(old_mbr):
				raise ValueError("MBR not found in parent block")
			
			# Insert the new mbrs to the parent block
			try:
				parent_block.insert(new_mbr1)  # old mbr was deleted so no overflow will not occur here
				parent_block.insert(new_mbr2)  # overflow may occur here
			except OverflowError:
				path.pop(-1)  # remove the last block, mbr from the path
				self.split_node(parent_block, path)
			
			
	def delete(self, record: Record):
		"""
		:param record: Record object to delete
		:return: None
		"""
		pass



	def range_query(self, area: BoundingArea) -> list[Record]:
		"""
		:param corners: A list of (d-1)-dimensional rectangle's corners
		:return: List of records included in the range query

		2d: corners = [(x1, y1), (x2, y2)]
		3d: corners = [(x1, y1, z1), (x2, y2, z2)]
		"""
		results: list[Record] = []
		stack = [self.root]
		while len(stack) > 0:
			print("Stack: ")
			for elem in stack:
				print(elem, sep=" ")
			print()
			node = stack.pop()  # pop the last element / index = -1 by default
			if node.is_leaf:  # node is leaf, so it contains records
				for record in node.elements:
					if area.point_in_area(record.location):  # check if the record is in the query area
						results.append(record)
			else:  # node is non-leaf, so it contains bounding areas
				for mbr in node.elements:
					if area.area_overlap(mbr) > 0:  # area_overlap returns the overlap area so it needs to be greater than zero
						stack.append(mbr.next_block)
		return results


	def nearest_neighbors(self, point: tuple, k: int) -> list[Record]:
		"""
		:param record: A tuple of location coordinates
		:return: k Records which are the nearest neighbors to the given point
		"""
		heap = []  # to work as a max heap
		heapq.heapify(heap)

		def recursion(node):
			if len(heap) == 0:
				radius = float('inf')
			else:
				radius = (-1) * heap[0].distance # heap[0] is the k-th nearest neighbor / ItemTuple object / weird stuff

			if node.is_leaf:
				for record in node.elements:
					distance = knn.eucl_distance(point, record.location)
					knn.add_to_heap(heap, (record, (-1) * distance), k)  # multiply with (-1) to have it work as a max heap
					# the record is added to the heap only if the distance is smaller than the radius (k-th nearest neighbor)
			else:
				sorted_mbrs = [(mbr, mbr.min_dist_from_point(point)) for mbr in node.elements]
				sorted_mbrs = sorted(sorted_mbrs, key=lambda x: x[1])
				for item in sorted_mbrs:
					mbr = item[0]
					distance = item[1]
					if distance < radius:  # if the distance is greater than the distance of the k-th nearest neighbor
						recursion(mbr.next_block)

		recursion(self.root)
		results = [(item.record, (-1) * item.distance) for item in heap]
		return sorted(results, key=lambda x: x[1])
		


	def bottomUp(self, records: list[Record]):
		"""
		:param records: A list of point coords
		:return: None
		"""
		pass


	def __str__(self):
		first_two_levels = ""
		first_two_levels += "Root: " + str(self.root) + "\n"
		if not self.root.is_leaf:
			for i, mbr in enumerate(self.root.elements):
				first_two_levels += f"Child {i+1} \n {str(mbr.next_block)} + \n"
		return first_two_levels