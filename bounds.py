from record import Record
import numpy as np

class Bounds:
    def __init__(self, lower, upper):
        if lower < upper:
            self.lower = lower
            self.upper = upper  
        else:  # just in case the bounds are in the wrong order
            self.lower = upper
            self.upper = lower
    
    

    def __str__(self):
        return f"Bounds: {self.lower} - {self.upper}"


   