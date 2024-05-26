class Record:
  def __init__(self, id: int, location: tuple, recID: int, name = ""):
    self.id = id
    self.location = location
    self.recID = recID
    self.name = name
    self.z_value = -1  # z-value for the specific record
    # αριθμός block στο οποίο ανήκει το Record στο δίσκο - υπολογίζεται στο parsing του osm/xml αρχείου    

  # Μέθοδος για να μπορεί η μέθοδος dumps του json να κάνει serialize αντικείμενα της κλάσης Record
  def to_dict(self):
    return {'id': self.id, 'location': self.location, 'recID': self.recID}
  
  # Για να μπορούμε να κάνουμε print τα Records
  def __str__(self):
      return f"Id: {self.id}, Location: {self.location}, recID: {self.recID}. Name: {self.name}. z-value: {self.z_value}"


  def __lt__(self, other):
        return False