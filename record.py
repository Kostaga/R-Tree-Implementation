import sys

class Record:
  obj_size = 0
  block_size = 1024 * 32

  def __init__(self, id: int, location: tuple, recID: int):
    self.id = id
    self.location = location
    self.recID = recID  
    # αριθμός block στο οποίο ανήκει το Record στο δίσκο - υπολογίζεται στο parsing του osm/xml αρχείου
  
  # static method to define block size
  @staticmethod
  def define_block_size(id: int, location: tuple) -> None:
    Record.obj_size = sys.getsizeof(id)  # bytes of id
    Record.obj_size += sys.getsizeof(location)  # bytes of location
    Record.block_size = Record.block_size // Record.obj_size

  # Μέθοδος για να μπορεί η μέθοδος dumps του json να κάνει serialize αντικείμενα της κλάσης Record
  def to_dict(self):
    return {'id': self.id, 'location': self.location, 'recID': self.recID}
  
  # Για να μπορούμε να κάνουμε print τα Records
  def __str__(self):
      return f"Record id: {self.id}, location: {self.location}, recID: {self.recID}"


# Record1 = Record(1, (1.0, 2.0))
# Record.define_block_size(Record1.id, Record1.location)

# print("Size of object: ",Record.obj_size)
# print("Objects per block: ", (1024 * 32) // Record.obj_size)