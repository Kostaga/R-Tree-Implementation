import xml.etree.cElementTree as et
import os
from record import Record
import json
from block import Block
from location_name_generator import location_name_generator
from itertools import islice
import time


def parse_osm() -> list[Record]:
    '''
    Parse the OSM file and store the nodes in blocks. Each block is stored in a separate line
    in the json file 'datafile.json'. The first line of the file contains the 'magic' block which
    contains information about the number of records and the number of blocks. Each block contains
    a list of dictionaries, each dictionary represents a record.
    '''
    nodes = []  # Define nodes in the global scope

    # Τα osm αρχεια ειναι xml στη δομή αρα το μετονομάζω για να μην 
    # υπάρχει σύγχυση με τη βιβλιοθηκη που διαβαζει xml αρχεια
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
        

    magic_block['num_of_records'] = counter  # πόσα records έχουμε συνολικά - υπολογίστηκε στο parsing του osm/xml αρχείου
    magic_block['num_of_blocks'] = block_index
    # Ό,τι άλλη χρησιμη πληροφορία θέλουμε για τα blocks την αποθηκεύουμε εδώ

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

    # Return a list of the records
    return [record for block in nodes[1:] for record in block]


def read_block(block_index) -> tuple[list[dict], float]:
    start_time = time.time()
    with open('datafile.json', 'r') as file:
        block = next(islice(file, block_index, block_index + 1))
        end_time = time.time()
        return json.loads(block), end_time - start_time
    


def delete_record(id, block_index: int) -> None:
    '''
    Delete the record with the given ID from the block with the given index
    '''
    start_time = time.time()
    block: list[dict] = read_block(block_index)[0]
    # Remove the record with the given ID
    for record in block:
        if record['id'] == id:
            block.remove(record)
            break

    # Write the block back to the file
    block = json.dumps(block)

    with open('datafile.json', 'r') as read_file:
        lines = read_file.readlines()
    with open('datafile.json', 'w') as file:
        counter = 0
        for line in lines:
            if counter == block_index:
                file.write(block + "\n")
            else:
                # line = json.loads(line)
                # line = json.dumps(line)
                file.write(line)
            counter += 1
    
    end_time = time.time()
    return end_time - start_time


        