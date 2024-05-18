from bounding_area import BoundingArea
from record import Record
from block import Block
from R_tree import RTree
from bounds import Bounds


record1 = Record(1, (5, 5), 1)
record2 = Record(2, (8, 3), 1)
record3 = Record(3, (4, 10), 2)
record4 = Record(4, (5, 3), 2)
record5 = Record(5, (16, 13), 2)
record6 = Record(6, (17, 14), 2)
record7 = Record(7, (22, 14), 2)
record8 = Record(8, (23, 15), 2)
record9 = Record(9, (24, 16), 2)
record10 = Record(10, (25, 17), 2)
record11 = Record(11, (26, 18), 2)
r_tree = RTree()
r_tree.insert_data(record1)
r_tree.insert_data(record2)
r_tree.insert_data(record3)
r_tree.insert_data(record4)

r_tree.insert_data(record5)
r_tree.insert_data(record6)
r_tree.insert_data(record7)
r_tree.insert_data(record8)
r_tree.insert_data(record9)
r_tree.insert_data(record10)

print(r_tree)
r_tree.delete(record1)
r_tree.delete(record2)
r_tree.delete(record3)
r_tree.delete(record4)
r_tree.delete(record5)
print(r_tree)


