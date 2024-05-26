import time
from R_tree import RTree
from record import Record
from memory_manager import parse_osm
from bounds import Bounds
from bounding_area import BoundingArea

def insert_records(r_tree,records):
	start_time = time.time()
	for i in range(500):
		r_tree.insert_data(records[i])
	
	calculate_time(start_time, "Insertion")


def delete_records(r_tree, records):
	start_time = time.time()
	for i in range(100):
		r_tree.delete(records[i])
	
	calculate_time(start_time, "Deletion")


def range_query(r_tree, range):
	start_time = time.time()
	r_tree.range_query(range)
	calculate_time(start_time, "Range query")

def linear_range_query(records, range):
	start_time = time.time()
	results: list[Record] = []
	for record in records:
		if range.point_in_area(record.location):
			results.append(record)

	calculate_time(start_time, "Linear Range query")


def knn_query(r_tree):
	start_time = time.time()
	r_tree.nearest_neighbors((1,3),100)
	calculate_time(start_time, "KNN query")

def skyline_query(r_tree):
	start_time = time.time()
	r_tree.skyline_query()
	calculate_time(start_time, "Skyline")

def bottom_up_construction(r_tree, records):
	start_time = time.time()
	r_tree.bottomUp(records[:1000])
	calculate_time(start_time, "Bottom-up construction")

def calculate_time(start_time, operation_name=""):
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(f"{operation_name} operation completed in {elapsed_time} seconds.")

def main():

	r_tree = RTree()
	records = parse_osm()

	insert_records(r_tree, records)
	delete_records(r_tree, records)
	range_query(r_tree, BoundingArea([Bounds(1.0, 100.0), Bounds(1.0, 100.0)], None))
	linear_range_query(records, BoundingArea([Bounds(1.0, 100.0), Bounds(1.0, 100.0)], None))
	knn_query(r_tree)
	skyline_query(r_tree)
	bottom_up_construction(r_tree, records)
	
	

if __name__ == "__main__":
	main()