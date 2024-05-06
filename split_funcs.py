from block import Block
from bounding_area import BoundingArea
from record import Record
import variables as var


def distribution_generator(lista: list):  # assumes the block is overflowed and has M+1 records (!!!!!!!!!)
    # lista is a list of records or a list of mbrs
    # Generator that yields all the M-2m+2 distributions of the block

    # Initialize the distribution
    first_half = []
    second_half = []
    # Iterate over the elements in the block
    min = var.MIN_ELEMENTS
    max = var.MAX_ELEMENTS
    index = min  # index to split the list
    # first_half = block.elements[:index]
    # second_half = block.elements[index:]
    
    first_half = lista[:index]
    second_half = lista[index:]

    for i in range(max - 2 * min + 2):
        # Yield the distribution
        yield first_half, second_half
    
        # Update the first half
        first_half.append(lista.elements[index])

        # Update the second half
        second_half = lista.elements[index + 1:]

        index += 1


def sort_all_dimensions_leaf(block: Block):
    if not block.is_leaf:
        raise ValueError("The block is not a leaf block")
    
    # Sort by all the dimensions of the block
    sorted_records = []
    for dim in range(var.DIMENSIONS):
        # Sort the elements of the block by the i-th dimension
        sorted_records.append(sorted(block.elements, key=lambda x: x.location[dim]))
    return sorted_records  # list of lists of records sorted by each dimension


def sort_all_dimensions_non_leaf(block: Block):
    if block.is_leaf:
        raise ValueError("The block is a leaf block")
    
    # Sort by all the dimensions of the block
    lower_bounds_sorted_mbrs = []
    upper_bounds_sorted_mbrs = []
    for dim in range(var.DIMENSIONS):
        # Sort the elements of the block by the i-th dimension frist by lower bounds and then by upper bounds
        lower_bounds_sorted_mbrs.append(sorted(block.elements, key=lambda x: x.bounds[dim].lower))
        upper_bounds_sorted_mbrs.append(sorted(block.elements, key=lambda x: x.bounds[dim].upper))
    return lower_bounds_sorted_mbrs, upper_bounds_sorted_mbrs  # tuple of lists of mbrs sorted by each dimension


def choose_split_axis_leaf(block: Block):
    '''
    Choose the axis to split the leaf block at
    Returns the axis with the smallest margin sum
    '''
    if not block.is_leaf:
        raise ValueError("The block is not a leaf block")
    
    sorted_records = sort_all_dimensions_leaf(block)
    margin_sums = [0] * var.DIMENSIONS
    for dim in range(var.DIMENSIONS):
        # Compute S for each dimension --> sum of all margin-values of the different distributions for each dimension
        # margin-value = margin[bb(first group)] + margin[bb(second group)]
        for dist in distribution_generator(sorted_records):
            # dist : tuple of two lists of records
            # Compute the bounding box of the first group
            first_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[0]), None) 
            # Compute the bounding box of the second group
            second_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[1]), None) 
            # Compute the margin-value of the bounding boxes
            margin_value = first_group.margin + second_group.margin
            # Update the sum of the margins
            margin_sums[dim] += margin_value
    # Choose the dimension with the smallest margin sum
    split_axis = margin_sums.index(min(margin_sums))
    return split_axis


def choose_split_axis_non_leaf(block: Block):
    '''
    Choose the axis to split the non-leaf block at (contains mbrs)
    Returns the axis with the smallest margin sum
    '''
    if block.is_leaf:
        raise ValueError("The block is a leaf block")
    
    sorted_mbrs_lower, sorted_mbrs_upper = sort_all_dimensions_non_leaf(block)
    margin_sums_lower = [0] * var.DIMENSIONS
    margin_sums_upper = [0] * var.DIMENSIONS
    for dim in range(var.DIMENSIONS):
        # Compute S for each dimension --> sum of all margin-values of the different distributions for each dimension
        # margin-value = margin[bb(first group)] + margin[bb(second group)]
        for dist in distribution_generator(sorted_mbrs_lower[dim]):
            # dist : tuple of two lists of records
            # Compute the bounding box of the first group
            first_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[0]), None) 
            # Compute the bounding box of the second group
            second_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[1]), None) 
            # Compute the margin-value of the bounding boxes
            margin_value = first_group.margin + second_group.margin
            # Update the sum of the margins
            margin_sums_lower[dim] += margin_value

        # Repeat for the upper bounds
        for dist in distribution_generator(sorted_mbrs_upper[dim]):
            first_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[0]), None) 
            second_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[1]), None) 
            margin_value = first_group.margin + second_group.margin
            margin_sums_lower[dim] += margin_value
            
    # Choose the dimension with the smallest margin sum
    index_lower = margin_sums_lower.index(min(margin_sums_lower))
    index_upper = margin_sums_upper.index(min(margin_sums_upper))
    
    if margin_sums_lower[index_lower] < margin_sums_upper[index_upper]:
        split_axis = index_lower
    else:   
        split_axis = index_upper
    return split_axis  # --> integer --> dimension index


def choose_split_index_leaf(split_axis: int, block: Block):
    '''
    Choose the index to split the block at
    Returns the best distribution of the elements of the block as a tuple of two lists of records
    '''
    if not block.is_leaf:
        raise ValueError("The block is not a leaf block")
    
    # Sort the elements of the block by the split axis
    sorted_block = sorted(block.elements, key=lambda x: x.location[split_axis])
    # Find the index to split the block
    min_overlap_value = float('inf')
    min_area_value = float('inf')  # to resolve ties of min overlap
    best_distribution = None
    for dist in distribution_generator(block):
        # dist : tuple of two lists of records
        # Compute the bounding box of the first group
        first_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[0]), None)
        # Compute the bounding box of the second group
        second_group = BoundingArea(BoundingArea.find_bounds_of_records(dist[1]), None)
        # Compute the overlap between the bounding boxes
        overlap_value = first_group.area_overlap(second_group)

        if overlap_value < min_overlap_value:
            # new best distribution
            min_overlap_value = overlap_value
            min_area_value = first_group.area + second_group.area
            best_distribution = dist
        elif overlap_value == min_overlap_value:  # resolve ties
            area_value = first_group.area + second_group.area
            if area_value < min_area_value:
                # new best distribution
                min_area_value = area_value
                best_distribution = dist
    return best_distribution  # tuple[list[Record], list[Record]]


def choose_split_index_non_leaf(split_axis: int, block: Block):
    '''
    Choose the index to split the block at (contains mbrs)
    Returns the best distribution of the elements of the block as a tuple of two lists of mbrs
    '''
    if block.is_leaf:
        raise ValueError("The block is a leaf block")
    
    # Sort the elements of the block by the split axis
    sorted_mbrs_lower = sorted(block.elements, key=lambda x: x.bounds[split_axis].lower)
    sorted_mbrs_upper = sorted(block.elements, key=lambda x: x.bounds[split_axis].upper)
    # Find the index to split the block
    min_overlap_value = float('inf')
    min_area_value = float('inf')  # to resolve ties of min overlap
    best_distribution = None
    for dist in distribution_generator(sorted_mbrs_lower):
        # dist : tuple of two lists of records
        # Compute the bounding box of the first group
        first_group = BoundingArea(BoundingArea.find_bounds_of_areas(dist[0]), None)
        # Compute the bounding box of the second group
        second_group = BoundingArea(BoundingArea.find_bounds_of_areas(dist[1]), None)
        # Compute the overlap between the bounding boxes
        overlap_value = first_group.area_overlap(second_group)

        if overlap_value < min_overlap_value:
            # new best distribution
            min_overlap_value = overlap_value
            min_area_value = first_group.area + second_group.area
            best_distribution = dist
        elif overlap_value == min_overlap_value:  # resolve ties
            area_value = first_group.area + second_group.area
            if area_value < min_area_value:
                # new best distribution
                min_area_value = area_value
                best_distribution = dist

    # Repeat for upper bound - distributions
    for dist in distribution_generator(sorted_mbrs_upper):
        # dist : tuple of two lists of records
        # Compute the bounding box of the first group
        first_group = BoundingArea(BoundingArea.find_bounds_of_areas(dist[0]), None)
        # Compute the bounding box of the second group
        second_group = BoundingArea(BoundingArea.find_bounds_of_areas(dist[1]), None)
        # Compute the overlap between the bounding boxes
        overlap_value = first_group.area_overlap(second_group)

        if overlap_value < min_overlap_value:
            # new best distribution
            min_overlap_value = overlap_value
            min_area_value = first_group.area + second_group.area
            best_distribution = dist
        elif overlap_value == min_overlap_value:  # resolve ties
            area_value = first_group.area + second_group.area
            if area_value < min_area_value:
                # new best distribution
                min_area_value = area_value
                best_distribution = dist
    return best_distribution  # tuple[list[Record], list[Record]]

if __name__ == '__main__':
    pass