from partition import Partition
from username import get_username
from graph import DotGraph
from clusterinfo import ClusterInfo
import partition
            
username = get_username()
f = open("/home/" + username + "/nodelist")

in_string = raw_input().split()
partition_name = ""

for split_string in in_string:
        if split_string.startswith("partition="):
            partition_name = split_string[len("partition="):]
            break

nodelist = f.readlines()
f.close()
#del(nodelist[0])

cluster_info = ClusterInfo(nodelist[1:])

all_nodes_sorted = cluster_info.get_partition_nodes(partition_name)

nodes_in_partition_file = open("/home/" + username + "/nodes",'w')

for i in xrange(len(all_nodes_sorted)):
    nodes_in_partition_file.write(all_nodes_sorted[i] + \
                                   (',' if i != len(all_nodes_sorted) - 1 else ''))
nodes_in_partition_file.close()

DotGraph(open("/home/" + username + "/nodes").readline()).print_graph()


    

