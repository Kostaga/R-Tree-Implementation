from record import Record
from R_tree import RTree
from bounds import Bounds
from block import Block
from bounding_area import BoundingArea


record1 = Record(1, (5, 5), 1)
record2 = Record(2, (8, 3), 1)
record3 = Record(3, (4, 10), 1)
record4 = Record(4, (5, 3), 1)
# record5 = Record(5, (16, 13), 2)
# record6 = Record(6, (17, 14), 2)
# record7 = Record(7, (22, 14), 2)
# record8 = Record(8, (23, 15), 2)
# record9 = Record(9, (24, 16), 2)
# record10 = Record(10, (25, 17), 2)

r_tree = RTree()

records_list = [record1, record2, record3, record4]

returned_records = r_tree.z_order_curve(records_list)

for item in returned_records:
	print(item.z_value)

