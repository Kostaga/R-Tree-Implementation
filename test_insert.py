from bounding_area import BoundingArea
from record import Record
from block import Block
from R_tree import RTree
from bounds import Bounds
from memory_manager import parse_osm
import time

if __name__ == '__main__':
    records = parse_osm()
    print("Parsed records")
    print(len(records))
    r_tree = RTree()
    start_time = time.time()
    for i, record in enumerate(records[:1000]):
        print(i)
        r_tree.insert(record)
   
    print("Insertion time: ", time.time() - start_time)
    print("Tree: ", r_tree)

    # query_area = BoundingArea([Bounds(3.5, 5), Bounds(2.5, 5)], None)
    # for record in r_tree.range_query(query_area):
    #     print("RANGE QUERY: ",record) 



