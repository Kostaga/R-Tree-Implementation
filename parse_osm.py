import string
import xml.etree.cElementTree as et
import os
from record import Record
import json
from block import Block
import random
from location_name_generator import location_name_generator


if __name__ == "__main__":
    nodes = []  # Define nodes in the global scope

    # Τα osm αρχεια ειναι xml απο οσο καταλαβαινω αρα το μετονομάζω για να μην 
    # υπάρχει σύγχυση με τη βιβλιοθηκη που διαβαζει xml
    # os.rename('map.osm', 'map.xml')  

    try:
        tree=et.parse('map.xml')
    except FileNotFoundError:
        os.rename('map.osm', 'map.xml')
        tree=et.parse('map.xml')

    root=tree.getroot()



    # Προσθέτω ένα magic block ως πρώτο "block0" της λίστας nodes
    magic_block = {}
    nodes.append(magic_block)

    counter = 0  # κάθε φορα που φτάνω στο block_size αυξάνω το block_index (δηλ. counter % block_size == 0)
    block_index = 1  # πρώτα αποθηκεύω στο block 1
    block_size = Block.max  # Μέγεθος block
    nodes.append([])  # πρώτο block

    for element in root.iter('node'):
        counter += 1
        if counter % block_size == 0:  # μηδενίζεται κάθε |block_size| επαναλήψεις
            block_index += 1
            nodes.append([])  # επόμενο block αποθήκευσης
        
        id = int(element.attrib['id'])
        location = (float(element.attrib['lat']), float(element.attrib['lon']))
        recID = block_index  # Αποθήκευση του node στο block που δείχνει το block_index
        # Generate a random name for the record
        loc_name = location_name_generator()
        
        nodes[block_index].append(Record(id, location, recID, name=loc_name))
        

    magic_block['num_of_nodes'] = counter  # πόσα nodes έχουμε συνολικά - υπολογίστηκε στο parsing του osm/xml αρχείου
    magic_block['num_of_blocks'] = block_index
    # Ό,τι άλλη χρησιμη πληροφορία θέλουμε για τα blocks την αποθηκεύουμε εδώ

    # Εκτύπωση των nodes
    for i in range(1, 5):
        print("Block: ", i, "Number of nodes: ", len(nodes[i]))
        for j in range(len(nodes[i])):
            print(nodes[i][j], "Block: ", i, "Node: ", j)


    # Convert the 'nodes' list to JSON format and dump each block seperately
    magic_block = json.dumps(magic_block)
    nodes_json = []
    for i in range(1, len(nodes)):  # json dumps μαγειες (πρεπει να γινει καθε αντικειμενο dict για να γινει serialize)
        nodes_json.append(json.dumps([node.to_dict() for node in nodes[i]]))

    # Save the JSON data to a file
    with open('datafile.json', 'w') as file:
        # First line is the magic block
        file.write(magic_block + "\n")

        # Writing each block separately so i can load them separately later
        for i in range(len(nodes_json)):
            file.write(nodes_json[i] + "\n")  



    # Επαναφορά του 2ου block δεδομένων του αρχείου datafile.json - για "εκπαιδευτικούς" σκοπούς
    from itertools import islice
    def read_block(block_index):
        with open('datafile.json', 'r') as file:
            block = next(islice(file, block_index, block_index + 1))
            return json.loads(block)


    print("Block 2: ", read_block(2))

    # nodes = []
    # nodes.append(magic_block)
    # for i in range(len(nodes_json)):
    #     nodes.append([Record(node1['id'], node1['location'], node1['recID']) for node1 in nodes_json[i]])


    # for i in range(1, len(nodes)):
    #     for j in range(len(nodes[i])):
    #         print(nodes[i][j], "Block: ", i, "Node: ", j)


