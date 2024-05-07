from math import floor

# for testing purposes, BLOCKSIZE was set to 1280 --> 5 records per block
# which means:
# MAX_ELEMENTS = 5
# MIN_ELEMENTS = 2

BLOCKSIZE = 1280  
RECORDSIZE = 256

INPUTFILE = "map.xml"
DATAFILE = "datafile.json"

M = 0.4 # Best performance has been experienced with M between 0.3-0.4 
P = 0.3 # p = 30% of M for leaf nodes as well as for nonleaf nodes yields the best performance (page 6)

MAX_ELEMENTS: int = floor(BLOCKSIZE // RECORDSIZE)
MIN_ELEMENTS: int = floor(M * MAX_ELEMENTS)

DIMENSIONS = 2