import sys

class Record:
  obj_size = 0
  block_size = 1024 * 32

  def __init__(self, id: int, location: tuple, recID: int, name = ""):
    self.id = id
    self.location = location
    self.recID = recID
    self.name = name
    self.z_value = -1  # z-value for the specific record
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
      return f"Id: {self.id}, Location: {self.location}, recID: {self.recID}. Name: {self.name}. z-value: {self.z_value}"


  def __lt__(self, other):
        return False