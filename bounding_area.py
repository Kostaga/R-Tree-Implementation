from bounds import Bounds
from record import Record
from block import Block
import numpy as np
from copy import deepcopy


class BoundingArea:
    def __init__(self, bounds: list[Bounds], next_block: Block):
        self.bounds = bounds
        self.next_block = next_block
        self.area = self.calculate_area()
        self.margin = self.calculate_margin()

    def calculate_area(self):
        '''
        Calculate the area of the bounding area
        '''
        area = 1
        for bound in self.bounds:
            area *= bound.upper - bound.lower
        return area
    
    def calculate_margin(self):
        '''
        Calculate the margin of the bounding area
        '''
        margin = 0
        for bound in self.bounds:
            margin += bound.upper - bound.lower
        return margin
    

    def point_in_area(self, point: tuple):  # takes a tuple of coordinates (record.location)
        '''
        Check if a point is within the bounding area
        '''
        for i, bound in enumerate(self.bounds):
            if point[i] < bound.lower or point[i] > bound.upper:
                return False
        return True
    
    def area_overlap(self, other: 'BoundingArea'):
        '''
        Calculate the overlap between two bounding areas
        '''
        for i, bound in enumerate(self.bounds):
            if bound.lower > other.bounds[i].upper or bound.upper < other.bounds[i].lower:
                return 0

        overlap = 1
        for i, bound in enumerate(self.bounds):
            overlap *= min(bound.upper, other.bounds[i].upper) - max(bound.lower, other.bounds[i].lower)
        
        return overlap

        
    
    def min_dist_from_point(self, point: tuple):
        '''
        Calculate the minimum distance from a point to the bounding area
        '''
        if self.point_in_area(point):  # If the point is in the area, the distance is 0
            return 0
        
        # Find the closest point in the bounding area to the given point
        clamped_point = [0] * len(self.bounds)
        for i in range(len(self.bounds)):
            if point[i] < self.bounds[i].lower:
                clamped_point[i] = self.bounds[i].lower
            elif point[i] > self.bounds[i].upper:
                clamped_point[i] = self.bounds[i].upper
            else:  # point[i] is within the bounds of the i-th dimension
                clamped_point[i] = point[i]

        # Calculate the distance between the clamped point and the given point
        distance = np.sqrt(np.sum(np.square(np.subtract(clamped_point, point))))
        return distance


    def include_point(self, record: Record) -> None:
        # Recaculate the bounds of the bounding area to include the record
        for dim, bound in enumerate(self.bounds):
            # dim --> dimension
            bound.lower = min(self.bounds[dim].lower, record.location[dim])
            bound.upper = max(self.bounds[dim].upper, record.location[dim])

        # Recalculate the area and margin of the bounding area
        self.area = self.calculate_area()
        self.margin = self.calculate_margin()


    def calculate_area_enlargement(self, record: Record) -> float:
        '''
        Calculate the area enlargement if the bounding area is expanded to include the record
        '''
        copy_mbr = deepcopy(self)
        copy_mbr.include_point(record)
        return copy_mbr.area - self.area
        

    def calculate_center(self):
        '''
        Calculate the center of the bounding area
        '''
        center = []
        for bound in self.bounds:
            center.append((bound.lower + bound.upper) / 2)
        return center
        

    def calculate_center_distance_leaf(self, record: Record):  # self is parent mbr, other is child record
        '''
        Calculate the distance between the center of the bounding area and the record
        '''
        center = self.calculate_center()
        return np.sqrt(np.sum(np.square(np.subtract(center, record.location))))


    def calculate_center_distance_non_leaf(self, other: 'BoundingArea'):  # self is parent mbr, other is child mbr
        '''
        Calculate the distance between the centers of two bounding areas
        '''
        center_self = self.calculate_center()
        center_other = other.calculate_center()
        return np.sqrt(np.sum(np.square(np.subtract(center_self, center_other))))


    @staticmethod
    def find_bounds_of_records(records: list[Record]):
        '''
        Find the bounds of a list of records
        '''
        records_arr = np.array([record.location for record in records])  # Convert the list of records to a numpy array for min/max to work
        min_values = np.min(records_arr, axis=0)  # Find the minimum values in each dimension
        max_values = np.max(records_arr, axis=0)  # Find the maximum values in each dimension

        bounds = [Bounds(min_values[i], max_values[i]) for i in range(len(min_values))]
        return bounds
    
    @staticmethod
    def find_bounds_of_areas(bounding_areas: list['BoundingArea']):
        '''
        Find the bounds of a list of bounding areas
        '''
        new_bounds = []
        for dimension in range(len(bounding_areas[0].bounds)):  # in need of a better way to find the number of dimensions
            # For each dimension, find the minimum and maximum values of the bounding areas
            min_values = np.min([bounding_area.bounds[dimension].lower for bounding_area in bounding_areas])
            max_values = np.max([bounding_area.bounds[dimension].upper for bounding_area in bounding_areas])
            new_bounds.append(Bounds(min_values, max_values))
    
        return new_bounds
    

    def __str__(self) -> str:
        return f"BB: {', '.join([f"{i+1}. {str(bound)}" for i, bound in enumerate(self.bounds)])}"
    
    
    
    