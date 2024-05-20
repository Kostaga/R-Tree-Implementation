from record import Record
from bounding_area import BoundingArea


def min_distance(element) -> float:
	if (isinstance(element, BoundingArea)):
		# if the element is an mbr, return the manhattan distance from of the lower-left corner to the origin
		x1 = element.bounds[0].lower
		y1 = element.bounds[1].lower
		return abs(x1) + abs(y1)
	else:
		# if the element is a record, return the manhattan distance from the record to the origin
		x = element.location[0]
		y = element.location[1]
		return abs(x) + abs(y)


def dominates(record1: Record, record2: Record) -> bool:
    '''
    record1 dominates record2.
    record1 dominates record2 if every coordinate of record1's location
    is less than or equal to the corresponding coordinate of record2's location,
    and there is at least one coordinate where record1's location is strictly less.
    '''
    is_strictly_better = False
    
    for r1, r2 in zip(record1.location, record2.location):
        if r1 > r2:
            return False
        if r1 < r2:
            is_strictly_better = True
    
    return is_strictly_better






