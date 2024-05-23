from record import Record
from R_tree import RTree
from bounds import Bounds
from block import Block
from bounding_area import BoundingArea
from zorder import z_order_curve
from memory_manager import parse_osm
import time

records = parse_osm()
# for rec in records:
#     print(rec)
r_tree = RTree()
start = time.time()
r_tree.bottomUp(records)
print(time.time() - start)
# print(r_tree)
