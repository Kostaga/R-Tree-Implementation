import heapq
import numpy as np
from record import Record


def eucl_distance(point1: tuple, point2: tuple) -> float:
    """
    :param point1: A tuple of location coordinates
    :param point2: A tuple of location coordinates
    :return: The distance between the two points
    """
    return np.linalg.norm(np.array(point1) - np.array(point2))


def add_to_heap(heap, item: tuple[Record, float], max_size: int):
    '''
    Add an item to a heap with a maximum size of max_size
    The min-heap is used with negative distances to the kNN query point and hence is used as a max-heap
    :param heap: The heap to add the item to
    :param item: The item to add, tuple that contains a Record and a float that is the distance to the kNN query point
    :param max_size: The maximum size of the heap
    '''
    class ItemTuple:
            '''
            Helper class to store a Record and a distance in a tuple.
            Sole purpose is to be used in the heap with functions that 
            override the comparison operators.
            '''
            def __init__(self, record: Record, distance: float):
                self.record = record
                self.distance = distance

            def __lt__(self, other):
                return self.distance < other.distance

            def __eq__(self, other):
                return self.distance == other.distance
    
    item = ItemTuple(item[0], item[1])
    distance = item.distance

    if len(heap) < max_size: # If the heap is not full, add the item
        heapq.heappush(heap, item)
    elif heap[0].distance < distance:
        # If the negative distance of the furthest neighbour (top element)
        # is smaller (larger by absolute values) replace it with the new item
        heapq.heappushpop(heap, item)