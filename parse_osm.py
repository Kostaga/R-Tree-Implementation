import xml.etree.cElementTree as et
import os
from record import Record
import json


if __name__ == "__main__":
    nodes = []  # Define nodes in the global scope

    # Τα osm αρχεια ειναι xml απο οσο καταλαβαινω αρα το μετονομάζω για να μην 
    # υπάρχει σύγχυση με τη βιβλιοθηκη που διαβαζει xml
    # os.rename('map.osm', 'map.xml')  


    tree=et.parse('map.xml')
    root=tree.getroot()



    # Προσθέτω ένα magic block ως πρώτο "block0" της λίστας nodes
    magic_block = {}
    nodes.append(magic_block)


    for element in root.iter('node'):
        # print(node.attrib)
        # στο module node η κλάση node με τη στατική μέθοδο... --> node.node...
        Record.define_block_size(int(element.attrib['id']), (float(element.attrib['lat']), float(element.attrib['lon'] ))) 
        # αντικείμενο που δεν αποθηκεύεται πουθενά (recID = -1)
        # το τρεχω μονο μία φορα για να γινουν initialized τα obj_size, block_size
        break


    counter = 0  # κάθε φορα που φτάνω στο block_size αυξάνω το block_index (δηλ. counter % block_size == 0)
    block_index = 1  # πρώτα αποθηκεύω στο block 1
    nodes.append([])  # πρώτο block

    for element in root.iter('node'):
        counter += 1
        if counter % Record.block_size == 0:  # μηδενίζεται κάθε [block_size] επαναλήψεις
            block_index += 1
            nodes.append([])  # επόμενο block αποθήκευσης
        
        id = int(element.attrib['id'])
        location = (float(element.attrib['lat']), float(element.attrib['lon']))
        recID = block_index  # Αποθήκευση του node στο block που δείχνει το block_index
        nodes[block_index].append(Record(id, location, recID))
        



    magic_block['num_of_nodes'] = counter  # πόσα nodes έχουμε συνολικά - υπολογίστηκε στο parsing του osm/xml αρχείου
    magic_block['num_of_blocks'] = block_index
    # Ό,τι άλλη χρησιμη πληροφορία θέλουμε για τα blocks την αποθηκεύουμε εδώ
        
    # print("Size of object: ", node.Node.obj_size, node.Node.block_size)
    # 84, 390 βγαίνουν τώρα που τα τρεχω

    # Εκτύπωση των nodes
    # for i in range(1, len(nodes)):
    #     for j in range(len(nodes[i])):
    #         print(nodes[i][j], "Block: ", i, "Node: ", j)


    # Convert the 'nodes' list to JSON format
    magic_block = json.dumps(magic_block)
    nodes_json = []
    for i in range(1, len(nodes)):  # json dumps μαγειες (πρεπει να γινει καθε αντικειμενο dict για να γινει serialize)
        nodes_json.append([node1.to_dict() for node1 in nodes[i]])
    nodes_json = json.dumps(nodes_json)

    # Save the JSON data to a file
    with open('datafile.json', 'w') as file:
        file.write(magic_block + "\n")
        file.write(nodes_json)



    # Επαναφορά του περιεχομένου του αρχείου datafile.json - για "εκπαιδευτικούς" σκοπούς
        
    # with open('datafile.json', 'r') as file:
    #     magic_block = json.loads(file.readline())
    #     nodes_json = json.loads(file.readline())

    # nodes = []
    # nodes.append(magic_block)
    # for i in range(len(nodes_json)):
    #     nodes.append([Record(node1['id'], node1['location'], node1['recID']) for node1 in nodes_json[i]])


    # for i in range(1, len(nodes)):
    #     for j in range(len(nodes[i])):
    #         print(nodes[i][j], "Block: ", i, "Node: ", j)


