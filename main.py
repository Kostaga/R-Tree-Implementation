import time
from R_tree import RTree
from record import Record
from memory_manager import parse_osm
from bounds import Bounds
from bounding_area import BoundingArea
import kNN_helper as knn
import heapq
import memory_manager as disc


def insert_records(r_tree: RTree, records: list[Record]):
	start_time = time.time()
	for i in range(500):
		r_tree.insert_data(records[i])
	
	calculate_time(start_time, "Insertion (500 records)")


def delete_records(r_tree: RTree, records: list[Record]):
	start_time = time.time()
	for i in range(100):
		r_tree.delete(records[i])
		disc.delete_record(records[i].id, records[i].recID)
	
	calculate_time(start_time, "Deletion")


def range_query(r_tree: RTree, range: BoundingArea):
	start_time = time.time()
	recordsFound = r_tree.range_query(range)

	# Read the records from the disk
	for record in recordsFound:
		disc.read_record(record.id, record.recID)
	
	calculate_time(start_time, "Range query")


def sequential_range_query(range: BoundingArea, records: list[Record]):
	start_time = time.time()
	recordsFound = []
	for record in records:
		if range.point_in_area(record.location):
			recordsFound.append(record)

	# Read the records from the disk
	for record in recordsFound:
		disc.read_record(record.id, record.recID)
	
	calculate_time(start_time, "Sequential Range query")


def knn_query(r_tree: RTree, point: tuple, k=10):
	start_time = time.time()
	recordsFound = [item[0] for item in r_tree.nearest_neighbors(point, k)]

	# Read the records from the disk
	for record in recordsFound:
		disc.read_record(record.id, record.recID)

	calculate_time(start_time, "KNN query")


def sequential_knn_query(point: tuple, records: list[Record], k=10):
	start_time = time.time()
	heap = []  # to work as a max heap
	heapq.heapify(heap)

	for record in records:
		distance = knn.eucl_distance(point, record.location)
		knn.add_to_heap(heap, (record, (-1) * distance), k)  # multiply with (-1) to have it work as a max heap
	
		results = [(item.record, (-1) * item.distance) for item in heap]
		results.sort(key=lambda x: x[1])
	
	# Read the records from the disk
	for record in results:
		disc.read_record(record[0].id, record[0].recID)
	
	calculate_time(start_time, "Sequential KNN query")


def skyline_query(r_tree: RTree):
	start_time = time.time()
	recordsFound = r_tree.skyline_query()

	# Read the records from the disk
	for record in recordsFound:
		disc.read_record(record.id, record.recID)

	calculate_time(start_time, "Skyline")


def bottom_up_construction(r_tree: RTree, records: list[Record]):
	start_time = time.time()
	r_tree.bottomUp(records[:500])
	calculate_time(start_time, "Bottom-up construction (500 records)")


def calculate_time(start_time, operation_name=""):
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(f"{operation_name} operation completed in {elapsed_time} seconds.")


def main():

	r_tree = RTree()
	records = parse_osm()

	insert_records(r_tree, records)
	delete_records(r_tree, records)

	r_tree = RTree()
	bottom_up_construction(r_tree, records)

	r_tree = RTree()
	r_tree.bottomUp(records)

	range_query(r_tree, BoundingArea([Bounds(40.6567365, 40.6598629), Bounds(22.9272785, 22.9485387)], None))
	sequential_range_query(BoundingArea([Bounds(40.6567365, 40.6598629), Bounds(22.9272785, 22.9485387)], None), records)

	knn_query(r_tree, (40.5, 22.9), 2)
	sequential_knn_query((40.5, 22.9) ,records, 2)
	skyline_query(r_tree)

	# Save the index file to the disk
	disc.save_indexfile(r_tree)

	
	
	

if __name__ == "__main__":
	main()