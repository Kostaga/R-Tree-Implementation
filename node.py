import sys

class Node:
  obj_size = 0
  block_size = 1024 * 32

  def __init__(self, id: int, location: tuple, recID: int):
    self.id = id
    self.location = location
    self.recID = recID  
    # αριθμός block στο οποίο ανήκει το node στο δίσκο - υπολογίζεται στο parsing του osm/xml αρχείου
  
  # static method to define block size
  @staticmethod
  def define_block_size(id: int, location: tuple) -> None:
    Node.obj_size = sys.getsizeof(id)  # bytes of id
    Node.obj_size += sys.getsizeof(location)  # bytes of location
    Node.block_size = Node.block_size // Node.obj_size

  # Μέθοδος για να μπορεί η μέθοδος dumps του json να κάνει serialize αντικείμενα της κλάσης Node
  def to_dict(self):
    return {'id': self.id, 'location': self.location, 'recID': self.recID}
  
  # Για να μπορούμε να κάνουμε print τα nodes
  def __str__(self):
      return f"Node id: {self.id}, location: {self.location}, recID: {self.recID}"


# node1 = Node(1, (1.0, 2.0))
# Node.define_block_size(node1.id, node1.location)

# print("Size of object: ",Node.obj_size)
# print("Objects per block: ", (1024 * 32) // Node.obj_size)