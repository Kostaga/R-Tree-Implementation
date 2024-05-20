from record import Record
from R_tree import RTree
from bounds import Bounds
from block import Block
from bounding_area import BoundingArea


a = Record(1, (1, 6), 1)
g = Record(2, (1, 4), 1)
b = Record(3, (3, 4), 1)
f = Record(4, (2, 2), 1)
c = Record(5, (4, 3), 1)
d = Record(6, (3, 1), 1)
e = Record(7, (5, 1), 1)



r_tree = RTree()

r_tree.insert_data(a)
r_tree.insert_data(g)
r_tree.insert_data(b)
r_tree.insert_data(f)
r_tree.insert_data(c)
r_tree.insert_data(d)
r_tree.insert_data(e)


results = r_tree.skyline_query()

for result in results:
	print(result)