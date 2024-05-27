import matplotlib.pyplot as plt
from R_tree import RTree
import time
from bounding_area import BoundingArea
from memory_manager import parse_osm
from bounds import Bounds
import memory_manager as disc


def plot_knn_times(r_tree: RTree, point: tuple):
    '''
    Plot the time taken to perform k-NN queries
    '''
    k_values = [i for i in range(5, 100, 3)]
    times = []
    for k in k_values:
        start_time = time.time()
        recordsFound = r_tree.nearest_neighbors(point, k)
        for record in recordsFound:
            disc.read_record(record[0].id, record[0].recID)
        end_time = time.time()
        times.append(end_time - start_time)

    plt.plot(k_values, times)
    plt.xlabel('k')
    plt.ylabel('Time (s)')
    plt.title('Time taken to perform k-NN query')
    plt.show()


def plot_range_query_times(r_tree: RTree):
    '''
    Plot the time taken to perform range queries
    '''
    range_factors = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
    range_mbr = BoundingArea([Bounds(40.63,  40.65), Bounds(22.9, 23.1)], None)

    times = []
    for range_factor in range_factors:
        for bound in range_mbr.bounds:
            bound.lower -= range_factor
            bound.upper += range_factor

        start_time = time.time()
        recordsFound = r_tree.range_query(range_mbr)
        for record in recordsFound:
            disc.read_record(record.id, record.recID)
        end_time = time.time()
        times.append(end_time - start_time)

    plt.plot(range_factors, times)
    plt.xscale('log')
    plt.xlabel('Range +- factor to lower and upper bounds')
    plt.ylabel('Time (s)')
    plt.title('Time taken to perform range queries')
    plt.show()


if __name__ == '__main__':
    r_tree = RTree()
    records = parse_osm()
    r_tree.bottomUp(records)

    plot_knn_times(r_tree, records[90].location)
    plot_range_query_times(r_tree)


    