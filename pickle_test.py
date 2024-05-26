import pickle

from R_tree import RTree
from memory_manager import parse_osm
import time

records = parse_osm()
r_tree = RTree()
start = time.time()
r_tree.bottomUp(records)
print(time.time() - start)
print(r_tree)

print("saving...")
print("saving...")
print("saving...")

with open('indexfile.bin', 'wb') as f:
    pickle.dump(r_tree, f)

print("saved")
print("saved")
print("saved")

print("loading...")
print("loading...")
print("loading...")

with open('indexfile.bin', 'rb') as f:
    r_tree = pickle.load(f)

print("loaded")
print("loaded")
print("loaded")
print(r_tree)

# IT WORKS