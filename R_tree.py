from record import Record
from block import Block
from bounding_area import BoundingArea
import variables
import area_overlap as avp

import numpy as np
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
			self.root = Block(is_leaf=True, levels=1)
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
		if (current_node.is_leaf):
			return current_node
		
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
			
			current_node = best_mbr.next_block

		# Current node has child pointers that point to leaves
		# Determine minimum area enlargement
		
		best_mbr = avp.calculate_least_overlap_enlargement(current_node, record)
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
