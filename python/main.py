from miniutils import get_username, del_pyc
from graph import DotGraph
from clusterinfo import ClusterInfo
            
username = get_username()
f = open("/home/" + username + "/nodelist")

args = raw_input().split()
partition_name = ""
topology_graph = 0

for current_arg in args:
        if current_arg.startswith("partition="):
            partition_name = current_arg[len("partition="):]
        elif current_arg == "-g" or "--graph":
            topology_graph = 1
        
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

if topology_graph:
    DotGraph(open("/home/" + username + "/nodes").readline()).print_graph()
    
del_pyc()


    

