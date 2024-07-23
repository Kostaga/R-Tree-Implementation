import numpy as np
import matplotlib.pyplot as plt
from bounding_area import BoundingArea
from R_tree import RTree
from record import Record
from block import Block
from memory_manager import parse_osm

# WORKS ONLY FOR TWO DIMENSIONS

def get_down_left_corner(mbr: BoundingArea):
    corner = []
    for bound in mbr.bounds:
        corner.append(bound.lower)  
    return corner

def get_rectangle_height(mbr: BoundingArea):
    return mbr.bounds[1].upper - mbr.bounds[1].lower


def get_rectangle_width(mbr: BoundingArea):
    return mbr.bounds[0].upper - mbr.bounds[0].lower


def visualize_tree(tree: RTree):
    # Initialize ploting space
    if tree.root.is_leaf:
        ploting_space = [[min([record.location[0] for record in tree.root.elements]), max([record.location[0] for record in tree.root.elements])], 
                         [min([record.location[1] for record in tree.root.elements]), max([record.location[1] for record in tree.root.elements])]]
    else:
        ploting_space = [[min([mbr.bounds[0].lower for mbr in tree.root.elements]), max([mbr.bounds[0].upper for mbr in tree.root.elements])], 
                         [min([mbr.bounds[1].lower for mbr in tree.root.elements]), max([mbr.bounds[1].upper for mbr in tree.root.elements])]]
    print(ploting_space)

    # Plot rectangles using a recursive function that traverses the tree
    fig, ax = plt.subplots()


    def recursion(current_node: Block):
        if current_node.is_leaf:
            # Plot records of leaf
            for record in current_node.elements:
                ax.scatter(*record.location, color='red')
            # points = [list(record.location) for record in current_node.elements]
            # ax.scatter(*zip(*points), color='red')
            return
        
        for i, mbr in enumerate(current_node.elements):
            corner = get_down_left_corner(mbr)
            ax.add_patch(plt.Rectangle(corner, get_rectangle_width(mbr), get_rectangle_height(mbr), fill=False, edgecolor='black'))
            ax.text(corner[0] + get_rectangle_width(mbr)/2, corner[1] + get_rectangle_height(mbr)/2, f'R{current_node.get_level()}{i}', fontsize=8, ha='center', va='center')
        for mbr in current_node.elements:
            recursion(mbr.next_block)


    # Initialize the recursion with the root node
    recursion(tree.root)

    # Set the plot limits and labels
    ax.set_xlim(ploting_space[0][0], ploting_space[0][1])
    ax.set_ylim(ploting_space[1][0], ploting_space[1][1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('R-tree visualization')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    tree = RTree()
    # Create 10 random records
    records = []
    for _ in range(15):
        id = np.random.randint(0, 100)
        location = np.random.rand(2)
        record = Record(id, location, -1)
        records.append(record)
    records = parse_osm()[:50]
    # Insert records into the R-tree
    tree.bottomUp(records)
    # Print the tree
    print(tree)

    # Visualize the tree
    visualize_tree(tree)
