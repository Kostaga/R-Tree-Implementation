from record import Record
from R_tree import RTree
from bounds import Bounds
from block import Block
from bounding_area import BoundingArea
from skyline_helper import dominates


a = Record(1, (1, 6), 1)
g = Record(2, (1, 4), 1)
b = Record(3, (3, 4), 1)
f = Record(4, (2, 2), 1)
c = Record(5, (40, 30), 1)
d = Record(6, (30, 10), 1)
e = Record(7, (50, 10), 1)



r_tree = RTree()

r_tree.insert_data(a)
r_tree.insert_data(g)
r_tree.insert_data(b)
r_tree.insert_data(f)
r_tree.insert_data(c)
r_tree.insert_data(d)
r_tree.insert_data(e)
print(r_tree)

results = r_tree.skyline_query()

for result in results:
	print(result)
