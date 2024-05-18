from record import Record
from R_tree import RTree
from bounds import Bounds
from block import Block
from bounding_area import BoundingArea
from zorder import z_order_curve




record1 = Record(1, (5, 5), 1)
record2 = Record(2, (8, 3), 1)
record3 = Record(3, (4, 10), 1)
record4 = Record(4, (5, 3), 1)
record5 = Record(5, (16, 13), 2)
record6 = Record(6, (17, 14), 2)
record7 = Record(7, (22, 14), 2)
record8 = Record(8, (23, 15), 2)
record9 = Record(9, (24, 16), 2)
record10 = Record(10, (25, 17), 2)
record11 = Record(11, (26, 18), 2)
record12 = Record(12, (27, 19), 2)
record13 = Record(13, (28, 20), 2)
record14 = Record(14, (29, 21), 2)
record15 = Record(15, (30, 22), 2)
record16 = Record(16, (31, 23), 2)
record17 = Record(17, (32, 24), 2)
record18 = Record(18, (33, 25), 2)
record19 = Record(19, (34, 26), 2)
record20 = Record(20, (35, 27), 2)
record21 = Record(21, (36, 28), 2)
record22 = Record(22, (37, 29), 2)
record23 = Record(23, (38, 30), 2)
record24 = Record(24, (39, 31), 2)
record25 = Record(25, (40, 32), 2)
record26 = Record(26, (41, 33), 2)
record27 = Record(27, (42, 34), 2)
record28 = Record(28, (43, 35), 2)
record29 = Record(29, (44, 36), 2)
record30 = Record(30, (45, 37), 2)
records = [record1, record2, record3, record4, record5, record6, record7, record8, record9, record10, record11, record12, record13, record14, record15, record16, record17, record18, record19, record20, record21, record22, record23, record24, record25, record26, record27, record28, record29, record30]
r_tree = RTree()
r_tree.bottomUp(records)
print(r_tree)