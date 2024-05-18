from record import Record
from block import Block
from bounding_area import BoundingArea
import variables
import area_overlap as avp
import split_funcs as sf

import heapq
import kNN_helper as knn


class RTree():

	level_overflow: set = set() # keep track of levels that have been overflowed
	
	def __init__(self, root=None):  # initialize root only for testing purposes
		self.root = Block(is_leaf=True, parent_mbr=None, parent_block=None) if root == None else root


	def insert_data(self, record):
		"""
		Insert data into the R-tree
		:param record: Record object to insert
		:return: None
		"""
		self.insert(record)

		RTree.level_overflow.clear()  # clear the set of levels that have been overflowed
	

	def insert(self, element, level = -1):  # level = -1 means that the element is a record
		"""
		:param element: Element may be a record or a boundingArea
		:return: None
		"""
		if (self.root == None):
			self.root = Block(is_leaf=True, parent_mbr=None, parent_block=None)
			self.root.insert(element)
			return
	
		re_insert_flag: bool = False
		
		# I1 Invoke ChooseSubtree. with the level as a parameter,
		# to find an appropriate node N, m which to place the
		# new entry E
		if level == -1:  # record is to be added
			node: Block = self.chooseSubtree(element)  # index 0 is the chosen leaf - index 1 is the path to the leaf
		else:
			node: Block = self.chooseSubtree(element, level)
		

		try:
			# If N has less than M entries, accommodate E in N
			self.adjust_insertion_path_mbrs(node, element)
			node.insert(element)  # OverflowError is raised if the block is full
		except OverflowError:
			# If N has M entries, invoke OverflowTreatment
			node_level = node.get_level()  # level of the leaf
			re_insert_flag = self.overflowTreatment(node_level)

			if (re_insert_flag): # If boolean variable is true, invoke reinsert
				self.reInsert(node)
			
			else: # else, split the node
				self.split_node(node)
				
			
	
	# 1) calculate mbr center
	# 2) calculate distance leaf

	def reInsert(self, block: Block):
		"""
		Reinsert the elements in the block.
		"""
		# percentage of M to be reinserted
		p = round(variables.P * variables.MAX_ELEMENTS)

		if (not block.is_leaf):
			# RI1 Compute the distance between the centers of their rectangles
			# and the center of the bounding rectangle of N
			pairs = []
			for element in block.elements:  # element is a bounding area
				distance = block.parent_mbr.calculate_center_distance_to_mbr(element) # calculate the distance between the center of the element and the center of the parent mbr
				pairs.append((element, distance))
			
			# RI2 Sort the entries in decreasing order of their distances
			pairs.sort(key=lambda x: x[1], reverse=True)
			pairs = [element for element, _ in pairs]  # now a list of only mbrs

			# RI3 Remove the first p entries from N 
			removed_entries = pairs[:p] # remove the first p entries
			remaining_entries = pairs[p:]  # remaining entries

			# adjust the bounding rectangle of N
			block.parent_mbr.bounds = BoundingArea.find_bounds_of_areas(remaining_entries)  # adjust the parent mbr of the block
			

			# RI4 in the sort defined in RI2, starting with the maximum distance
			# or minimum distance, invoke insert to reinsert the entries
			for mbr in removed_entries:
				block.elements.remove(mbr) # remove the entries from the block
			for mbr in removed_entries:
				self.insert(mbr, block.get_level()) # reinsert the entries



		else:
			# RI1 Compute the distance between the center of the rectangle and the center of the bounding rectangle of N
			pairs = []
			for element in block.elements:
				# Suspicous: calculate_center_distance_leaf is not a method of the Record class
				distance = block.parent_mbr.calculate_center_distance_to_record(element) # calculate the distance between the center of the element and the center of the parent mbr
				pairs.append((element, distance))
			
			pairs.sort(key=lambda x: x[1], reverse=True)
			pairs = [element for element, _ in pairs]  # now a list of only records

			# RI3 Remove the first p entries from N
			removed_entries = pairs[:p]
			remaining_entries = pairs[p:]

			# adjust the bounding rectangle of N
			block.parent_mbr.bounds = BoundingArea.find_bounds_of_records(remaining_entries)  # adjust the parent mbr of the block

			# RI4 in the sort defined in RI2, starting with the maximum distance
			# or minimum distance, invoke insert to reinsert the entries
			for record in removed_entries:
				block.elements.remove(record)
			for record in removed_entries:
				self.insert(record, block.get_level())
			
		

	def chooseSubtree(self, element, level = -1) -> tuple[Block,list[tuple[Block, BoundingArea]]]:
		"""
        Choose the subtree to insert the element based on 
		minimum overlap or area cost.
        """
		#CS1 Let N be the root
		current_node: Block = self.root

		#CS2 If N 1s a leaf, return N 
		if (current_node.is_leaf):
			return current_node

		
		# else
		# if the childpointers in N point to leaves, determine minimum overlap cost
		
		# Determine minimum overlap cost
		# Include point in the passing MBRs ???????
		if level == -1:  # record is to be added
			while not current_node.elements[0].next_block.is_leaf:
				# CS3 Choose the entry E from N that needs least area enlargement to include R
				min_area_enlargement = float('inf')
				best_mbr: BoundingArea = None
				mbr: BoundingArea = None  # type hinting for the for-loop
				for mbr in current_node.elements:
					area_enlargement = mbr.calculate_area_enlargement(element)
					if area_enlargement < min_area_enlargement or (area_enlargement == min_area_enlargement and mbr.area < best_mbr.area):
						min_area_enlargement = area_enlargement
						best_mbr = mbr

				current_node = best_mbr.next_block
				

			# Current node has child pointers that point to leaves
			# Determine minimum area enlargement
			
			best_mbr_index = avp.calculate_least_overlap_enlargement(current_node, element)
			chosen_leaf = current_node.elements[best_mbr_index].next_block

			return chosen_leaf
		
		else:  # element is mbr
			for i in range(level):
				# CS3 Choose the entry E from N that needs least area enlargement to include R
				min_area_enlargement = float('inf')
				best_mbr: BoundingArea = None
				mbr: BoundingArea = None
				for mbr in current_node.elements:
					area_enlargement = mbr.calculate_area_enlargement(element)
					if area_enlargement < min_area_enlargement or (area_enlargement == min_area_enlargement and mbr.area < best_mbr.area):
						min_area_enlargement = area_enlargement
						best_mbr = mbr
				
				current_node = best_mbr.next_block
			
			return current_node


	def overflowTreatment(self, level: int) -> bool:
		# OTl If the level 1s not the root level and this IS the first
		# call of OverflowTreatment m the given level
		# durmg the Insertion of one data rectangle, then
		if level != 0:  # if the level is not the root level --> level 0
			# Mark level as already inserted
			if (level not in RTree.level_overflow):
				RTree.level_overflow.add(level)
				return True
		return False
	
	
	def split_node(self, node: Block) -> None:
		"""
		Split node into two new nodes and insert the new mbrs to the parent block. Adjust the parent mbr of the parent block 
		to the new mbrs. If the parent block overflows, split it as well.
		:param node: Block to split
		:return: None
		"""

		# Create two new blocks and
		# connect the proper pointers up and down
		if node.is_leaf:  # node is a leaf and hence contains records
			split_axis = sf.choose_split_axis_leaf(node)
			splits = sf.choose_split_index_leaf(split_axis, node)

			new_node1 = Block(is_leaf=True, parent_mbr=None, parent_block=node.parent_block)  # New nodes are leaves
			new_node2 = Block(is_leaf=True, parent_mbr=None, parent_block=node.parent_block)	
			new_mbr1 = BoundingArea(bounds=BoundingArea.find_bounds_of_records(splits[0]), next_block=new_node1)  # next_block is the pointer to leaf1
			new_mbr2 = BoundingArea(bounds=BoundingArea.find_bounds_of_records(splits[1]), next_block=new_node2)  # next_block is the pointer to leaf2
			
		else:  # node is a non-leaf and hence contains bounding areas
			split_axis = sf.choose_split_axis_non_leaf(node)
			splits = sf.choose_split_index_non_leaf(split_axis, node)

			new_node1 = Block(is_leaf=False, parent_mbr=None, parent_block=node.parent_block)  # new nodes are non-leaves
			new_node2 = Block(is_leaf=False, parent_mbr=None, parent_block=node.parent_block)
			new_mbr1 = BoundingArea(bounds=BoundingArea.find_bounds_of_areas(splits[0]), next_block=new_node1)  # next_block is the pointer to leaf1
			new_mbr2 = BoundingArea(bounds=BoundingArea.find_bounds_of_areas(splits[1]), next_block=new_node2)  # next_block is the pointer to leaf2
			
		new_node1.parent_mbr = new_mbr1  # set the parent_mbr of leaf1 to the new mbr1 so wherever the mbr1 goes later in splits, leaf1 will "follow"
		new_node2.parent_mbr = new_mbr2
		new_node1.elements = splits[0]  # allocate the newlly split elements to the new nodes
		new_node2.elements = splits[1]

		if node.parent_block == None:  # at root level
			new_root = Block(is_leaf=False, parent_mbr=None, parent_block=None)  # new root is a non-leaf
			new_root.insert(new_mbr1)
			new_root.insert(new_mbr2)
			new_node1.parent_block = new_root
			new_node2.parent_block = new_root
			self.root = new_root
		else:
			# Delete the old mbr from the parent block
			parent_block: Block = node.parent_block
			old_mbr: BoundingArea = node.parent_mbr
			if not parent_block.delete(old_mbr):
				raise ValueError("MBR not found in parent block")
			
			# Insert the new mbrs to the parent and adjust the parent mbr of the parent block
			try:
				# No parent_mbr adjustment is needed here because the it was adjusted in the adjust_insertion_path_mbrs function
				parent_block.insert(new_mbr1)  # old mbr was deleted so no overflow will not occur here
				parent_block.insert(new_mbr2)  # overflow may occur here
				
			except OverflowError:
				parent_block_level = parent_block.get_level()  # level of the parent block
				re_insert_flag = self.overflowTreatment(parent_block_level)
				if (re_insert_flag):
					self.reInsert(parent_block)
				else:
					self.split_node(parent_block)
			
	
	
	def delete(self, record: Record):
		"""
		:param record: Record object to delete
		:return: None
		"""
		re_insertions = []  # list of reinserted elements
		re_insert_flag = False
		record_bounds = BoundingArea(bounds=BoundingArea.find_bounds_of_records([record]), next_block=None)

		# decrease upper bound and lower bound by 0.001 to avoid floating point errors
		for bound in record_bounds.bounds:
			bound.upper += 0.001
			bound.lower -= 0.001

		stack = [self.root]
		while len(stack) > 0:
			node = stack.pop()  # pop the last element / index = -1 by default
			if node.is_leaf:  # node is leaf, so it contains records
					node.elements.remove(record)
					node.parent_mbr.bounds = BoundingArea.find_bounds_of_records(node.elements)  # adjust the parent mbr of the node
					for element in node.elements:
						re_insertions.append(element)
					if len(node.elements) < variables.MIN_ELEMENTS:
						re_insert_flag = True
						for element in node.elements:
							node.elements.remove(element)
	
						# delete the mbr from the parent block
						node.parent_block.delete(node.parent_mbr)
						
					break
			else:  # node is non-leaf, so it contains bounding areas
				for mbr in node.elements:
					if record_bounds.area_overlap(mbr) > 0:  # area_overlap returns the overlap area so it needs to be greater than zero
						stack.append(mbr.next_block)
		
		# reinsert the elements that were left from the underflowed node
		if re_insert_flag:
			for element in re_insertions:
				self.insert_data(element)

		

	
	def adjust_insertion_path_mbrs(self, node: Block, element):
		"""
		Adjust the parent mbrs of the path to the inserted element.
		:return: None
		"""
		current_node = node
		while current_node.parent_block != None:
			parent_block: Block = node.parent_block
			parent_mbr: BoundingArea = node.parent_mbr
			if isinstance(element, Record):
				parent_mbr.include_point(element)
			else:
				parent_mbr.include_area(element)

			current_node = parent_block  # go up one level
		



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