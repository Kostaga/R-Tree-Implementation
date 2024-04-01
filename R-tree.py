from Record import Record
import Variables

class RTree():

	def __init__(self):
		self.nodeMaxEntries: int = (Variables.BLOCKSIZE // Variables.RECORDSIZE) #temporary I guess for now
		self.nodes = {"root": {"id": 0, "level": 0, "first_insert": True}}
		self.m: int = Variables.M * self.nodeMaxEntries
		"""
        nodes = {"root": {"id": 0, "level": 0},
                    1: {"id": 1, "level":0, "type": n, "rectangle" = []}...}
        """

	def insert(self, record: Record):
		"""
		:param record: Record object to insert
		:return: None
		"""
		
		# Step 1: Find the leaf node to insert the record. Invoke chooseLeaf to select a leaf node L in which to place the new record


		# Step 2: Add the record to the leaf node L. If L has room for another entry, install E. Otherwise, invoke SplitNode to obtain L and LL containing E and all the old entries of L


		# Step 3: Propagate changes upward. Invoke AdjustTre on L, also passing LL if a split was performed


		# Step 4: Grow tree taller. If node split propagation caused the root to split, create a new root whose children are the two resulting nodes






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
