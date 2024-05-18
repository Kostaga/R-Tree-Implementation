from bounding_area import BoundingArea
from record import Record
from block import Block
from R_tree import RTree
from bounds import Bounds

if __name__ == '__main__':
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





    r_tree: RTree = RTree()
    r_tree.insert_data(record1)
    r_tree.insert_data(record2)
    r_tree.insert_data(record3)
    r_tree.insert_data(record4)

    r_tree.insert_data(record5)
    r_tree.insert_data(record6)
    r_tree.insert_data(record7)
    print("Record 7 insert_dataed")
    r_tree.insert_data(record8)
    print("Record 8 insert_dataed")
    r_tree.insert_data(record9)
    print("Record 9 insert_dataed")


    r_tree.insert_data(record10)
    print("Record 10 insert_dataed")
    print(r_tree)

    query_area = BoundingArea([Bounds(3.5, 5), Bounds(2.5, 5)], None)
    for record in r_tree.range_query(query_area):
        print("RANGE QUERY: ",record) 



