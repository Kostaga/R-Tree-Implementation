from bounding_area import BoundingArea
from record import Record
from bounds import Bounds
from block import Block
import split_funcs as sf
from R_tree import RTree

from random import shuffle


if __name__ == '__main__':
    record1 = Record(1, (1.0, 12.0), 1)
    record2 = Record(2, (3.0, 10.0), 1)
    record3 = Record(3, (5.0, 8.0), 2)
    record4 = Record(4, (7.0, 6.0), 2)
    record5 = Record(5, (9.0, 10.0), 2)
    record6 = Record(6, (11.0, 12.0), 2)

    records = [record1, record2, record3, record4, record5, record6]
    shuffle(records)

    area1 = BoundingArea([Bounds(4.0, 9.0), Bounds(2.0, 6.0)], None)
    area2 = BoundingArea([Bounds(3.0, 7.0), Bounds(1.0, 14.0)], None)
    area3 = BoundingArea([Bounds(15.0, 20.0), Bounds(6.0, 15.0)], None)
    area4 = BoundingArea([Bounds(-12.0, 13.0), Bounds(-12.0, 20.0)], None)
    area5 = BoundingArea([Bounds(9.0, 11.0), Bounds(10.0, 14.0)], None)
    area6 = BoundingArea([Bounds(-5.0, 3.0), Bounds(3.0, 4.0)], None)

    areas = [area1, area2, area3, area4, area5, area6]
    shuffle(areas)


    
    # καπως ετσι να προσθετουμε γνκ στοιχεια στο block με το try except γτ τα split funcs θα το χρειαστουν το εξτρα overflowed record
    # block = Block(True, 0)
    # for rec in records:
    #     try:
    #         block.insert(rec)
    #     except ValueError:
    #         print("Block is full")
    #         print("Initiating split...")

    block = Block(False, 0)
    for area in areas:
        try:
            block.insert(area)
        except ValueError:
            print("Block is full")
            print("Initiating split...")

    

    

    # DISTRIBUTION GENERATOR TESTING
    # for dist1, dist2 in sf.distribution_generator(block.elements):
    #     print("dist1")
    #     for rec in dist1:
    #         print(rec)
    #     print("dist2")
    #     for rec in dist2:
    #         print(rec)


    # SPLIT FUNCTIONS TESTING
    
    # Sorting all dimensions

    # Records
    # sorted_dimensions: list = sf.sort_all_dimensions_leaf(block)
    # for i, dim in enumerate(sorted_dimensions):
    #     print(f"Dimension {i+1} sort")
    #     for rec in dim:
    #         print(rec)
    #     print("\n")

    # MBRs
    # mbrs_lower, mbrs_upper = sf.sort_all_dimensions_non_leaf(block)
    # print("Lower bound sorting")
    # for i, dim in enumerate(mbrs_lower):
    #     print(f"Dimension {i+1} lower")
    #     for mbr in dim:
    #         print(mbr)
    # print("\nUpper bound sorting")
    # for i, dim in enumerate(mbrs_upper):
    #     print(f"Dimension {i+1} upper")
    #     for mbr in dim:
    #         print(mbr)
        

    # ChooseSplitAxis

    # Records
    # split_axis = sf.choose_split_axis_leaf(block)
    # splits = sf.choose_split_index_leaf(split_axis, block)
    # print(f"Split axis: {split_axis}")
    # sf.print_dist_recs(splits)

    # MBRs
    split_axis = sf.choose_split_axis_non_leaf(block)
    splits = sf.choose_split_index_non_leaf(split_axis, block)
    print(f"Split axis: {split_axis}")
    sf.print_dist_mbrs(splits)

    # Δοκιμή πρακτικής για διασπαση leaf-block
    # new_leaf1 = Block(True, 0)
    # new_leaf1.elements = splits[0]
    # new_leaf2 = Block(True, 0)
    # new_leaf2.elements = splits[1]

    # bounds1 = BoundingArea.find_bounds_of_records(splits[0])
    # area1 = BoundingArea(bounds1, new_leaf1)

    # bounds2 = BoundingArea.find_bounds_of_records(splits[1])
    # area2 = BoundingArea(bounds2, new_leaf2)

    # new_node = Block(False, 0)
    # new_node.insert(area1)
    # new_node.insert(area2)

    # print(new_node.elements[0])
    # print(new_node.elements[1])

    # print("\nElements of leaf that is pointed by the first area:")
    # for rec in new_node.elements[0].next_block.elements:
    #     print(rec)

    # Δοκιμή πρακτικής για διασπαση node-block
    new_node1 = Block(False, 0)
    new_node1.elements = splits[0]
    new_node2 = Block(False, 0)
    new_node2.elements = splits[1]

    bounds1 = BoundingArea.find_bounds_of_areas(splits[0])
    area1 = BoundingArea(bounds1, new_node1)

    bounds2 = BoundingArea.find_bounds_of_areas(splits[1])
    area2 = BoundingArea(bounds2, new_node2)

    new_node = Block(False, 0)
    new_node.insert(area1)
    new_node.insert(area2)




    # # TESTING BOUNDING AREA
    # bound1 = Bounds(5, 10)
    # bound2 = Bounds(0, 10)
    # area1 = BoundingArea([bound1, bound2], None)
    # print(area1)

    # bound3 = Bounds(7, 20)
    # bound4 = Bounds(0,10)
    # area2 = BoundingArea([bound3, bound4], None)
    # areas = [area1, area2]

    # print(area1.point_in_area((11.0, 2.0)))  # False

    # print(area1.area_overlap(area2))  # 0

    # for bound in BoundingArea.find_bounds_of_records(records):
    #     print(bound)  # Bounds: 1.0 - 5.0, 2.0 - 6.0

    # for bound in BoundingArea.find_bounds_of_areas(areas):
    #     print(bound) # Bounds: 5 - 20, 0 - 10

    # print(area2.min_dist_from_point((0,10)))  # 7.0


