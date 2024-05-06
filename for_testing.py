from bounding_area import BoundingArea
from record import Record
from bounds import Bounds
import area_overlap


if __name__ == '__main__':
    # Assuming 'points' is your n x d list
    record1 = Record(1, (1.0, 2.0), 1)
    record2 = Record(2, (3.0, 4.0), 1)
    record3 = Record(3, (5.0, 6.0), 2)

    records = [record1, record2, record3]

    bound1 = Bounds(5, 10)
    bound2 = Bounds(0, 10)
    area1 = BoundingArea([bound1, bound2], None)

    bound3 = Bounds(7, 20)
    bound4 = Bounds(0,10)
    area2 = BoundingArea([bound3, bound4], None)
    areas = [area1, area2]

    print(area1.point_in_area((11.0, 2.0)))  # False

    print(area1.area_overlap(area2))  # 0

    for bound in BoundingArea.find_bounds_of_records(records):
        print(bound)  # Bounds: 1.0 - 5.0, 2.0 - 6.0

    for bound in BoundingArea.find_bounds_of_areas(areas):
        print(bound) # Bounds: 5 - 20, 0 - 10

    print(area2.min_dist_from_point((0,10)))  # 7.0
