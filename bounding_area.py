from Bounds import Bounds
from Record import Record
import numpy as np

class BoundingArea:
    def __init__(self, bounds: list[Bounds]):
        self.bounds = bounds

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
        Check if two bounding areas overlap
        '''
        for i, bound in enumerate(self.bounds):
            if bound.lower > other.bounds[i].upper or bound.upper < other.bounds[i].lower:
                return False
        return True
    
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

    
    @staticmethod
    def find_bounds_of_records(records: list[Record]):
        '''
        Find the bounds of a list of records
        '''
        records = np.array([record.location for record in records])  # Convert the list of records to a numpy array for min/max to work
        min_values = np.min(records, axis=0)  # Find the minimum values in each dimension
        max_values = np.max(records, axis=0)  # Find the maximum values in each dimension

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
    
    
    
    