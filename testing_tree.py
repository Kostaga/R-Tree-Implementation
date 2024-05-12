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
    
    records = [record1, record2, record3, record4, record5]

    area1 = BoundingArea([Bounds(4.0, 9.0), Bounds(2.0, 6.0)], None)
    area2 = BoundingArea([Bounds(3.0, 7.0), Bounds(1.0, 14.0)], None)
    area3 = BoundingArea([Bounds(15.0, 20.0), Bounds(6.0, 15.0)], None)
    area4 = BoundingArea([Bounds(-12.0, 13.0), Bounds(-12.0, 20.0)], None)
    area5 = BoundingArea([Bounds(9.0, 11.0), Bounds(10.0, 14.0)], None)
    area6 = BoundingArea([Bounds(-5.0, 3.0), Bounds(3.0, 4.0)], None)

    root = Block(False, None)  # root block
    # Leaf root
    # root.insert(record1)
    # root.insert(record2)
    # root.insert(record3)
    # root.insert(record4)
    # root.insert(record5)
    # root.insert(record6)

    # Non-leaf root
    root.insert(area1)
    root.insert(area2)
    root.insert(area3)
    root.insert(area4)
    root.insert(area5)
    # root.insert(area6)

    
    block1 = Block(True, area1)
    block2 = Block(True, area2)
    block3 = Block(True, area3)

    area1.next_block = block1
    area2.next_block = block2
    area3.next_block = block3
    
    block1.insert(record1)  # 5, 5
    block1.insert(record2)  # 8, 3

    block2.insert(record3)  # 4, 10
    block2.insert(record4)  # 5, 3

    block3.insert(record5)  # 16, 16
    block3.insert(record6)  # 17, 17


    # RANGE QUERY - IT WORKS
    # query_area = BoundingArea([Bounds(3.5, 5), Bounds(2.5, 5)], None)
    # print(query_area)
    # print("Range query:")
    # for record in r_tree.range_query(query_area):
    #     print(record) 


    # NEAREST NEIGHBORS - IT WORKS BUT IT IS WEIRD - NOT TO BE TOUCHED IN THE FUTURE FOR MENTAL REASONS
    # print("Nearest neighbors:")
    # for record, dist in r_tree.nearest_neighbors((5,4), 4):
    #     print(record)
    #     print(dist)


    #TESTING SPLIT NODE AS A WHOLE
    r_tree: RTree = RTree(root=root)  # root is a non-leaf block
    print(r_tree)
    print("After split:")
    try:
        root.insert(area6)
    except OverflowError:
        r_tree.split_node(root, [])
    
    print(r_tree)

