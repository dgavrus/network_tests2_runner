from partition import Partition
from username import get_username
from graph import DotGraph
            
username = get_username()
f = open("/home/" + username + "/nodelist")

in_string = raw_input().split(' ')
partition = ""

for split_string in in_string:
        if split_string.startswith("partition="):
            partition = split_string[len("partition="):]
            break

nodelist = f.readlines()
f.close()
del(nodelist[0])

partitions = []
if len(partition) > 0:
    for curr_part in nodelist:
        if(curr_part.startswith(partition) or partition == "all"):
            parameters = curr_part.split()  
            partitions.append(Partition(parameters[0],parameters[1], \
                                        parameters[2],parameters[3], \
                                        parameters[4],parameters[5]))
            
num_of_nodes_printed = 0
num_of_nodes_real = 0

for i in xrange(len(partitions)):
    print partitions[i].name, partitions[i].state
    print partitions[i].get_all_nodes()
    
all_nodes_sorted = []

for p in partitions:
    nodes = p.get_all_nodes()
    for node in nodes:
        if all_nodes_sorted.count(node) == 0:
            all_nodes_sorted.append(node)
        
all_nodes_sorted.sort(cmp=None, key=None, reverse=False)

nodes_in_partition_file = open("/home/" + username + "/nodes",'w')

for i in xrange(len(all_nodes_sorted)):
    nodes_in_partition_file.write(all_nodes_sorted[i] + \
                                  (',' if i != len(all_nodes_sorted) - 1 else ''))
nodes_in_partition_file.close()

graph = DotGraph(open("/home/" + username + "/nodes").readline())
graph.print_graph()
    

    

