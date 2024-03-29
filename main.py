import sys

class node:
  obj_size = 0
  def __init__(self, id: int, location: tuple):
    self.id = id
    self.location = location


def define_obj_size(id, location):
  node.obj_size = sys.getsizeof(id)  # bytes of id
  node.obj_size += sys.getsizeof(location)  # bytes of location


node1 = node(1, (1.0, 2.0))
define_obj_size(node1.id, node1.location)

print("Size of object: ",node.obj_size)
print("Objects per block: ", (1024 * 32) // node.obj_size)