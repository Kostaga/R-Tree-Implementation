BLOCKSIZE = 32 * 1024
RECORDSIZE = 256
ENTRYSIZE = 256
INPUTFILE = "map.xml"
DATAFILE = "datafile.json"
M = 0.4 # Best performance has been experienced with M between 0.3-0.4 
P = 0.3 # p = 30% of M for leaf nodes as well as for nonleaf nodes yields the best performance (page 6)

MAX_ELEMENTS: int = (BLOCKSIZE // RECORDSIZE)
MIN_ELEMENTS: int = M * MAX_ELEMENTS

DIMENSIONS = 2