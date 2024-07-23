import numpy as np
import matplotlib.pyplot as plt
from bounding_area import BoundingArea
from R_tree import RTree
from record import Record
from block import Block

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
    # Generate random points inside each square
    

    # Plot rectangles using a recursive function that traverses the tree
    fig, ax = plt.subplots()


    def recursion(current_node: Block):
        if current_node.is_leaf:
            # Plot records of leaf
            points = [list(record.location) for record in current_node.elements]
            ax.scatter(*zip(*points), color='red')
            return
        
        for mbr in current_node.elements:
            corner = get_down_left_corner(mbr)
            ax.add_patch(plt.Rectangle(corner, get_rectangle_width(mbr), get_rectangle_height(mbr), fill=False, edgecolor='black'))
        for mbr in current_node.elements:
            recursion(mbr.next_block)


    # Initialize the recursion with the root node
    recursion(tree.root)

    # Plot records / points
    # ax.scatter(*zip(*points), color='red')

    # Set the plot limits and labels
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('R-tree visualization')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    tree = RTree()
    # Create 10 random records
    records = []
    for _ in range(26):
        id = np.random.randint(0, 100)
        location = np.random.rand(2)
        record = Record(id, location, -1)
        records.append(record)

    # Insert records into the R-tree
    tree.bottomUp(records)

    # Print the tree
    print(tree)

    # Visualize the tree
    visualize_tree(tree)
