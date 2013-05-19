from miniutils import get_username, del_pyc, del_res
from graph import DotGraph
from clusterinfo import ClusterInfo
import subprocess, os
            
username = get_username()

del_res()

path = os.getcwd()[:os.getcwd().index(username) + len(username)]

#f = open(path + "/nodelist",'w')
#  
#subprocess.call(["sinfo"], stdout=f)
#  
#f.close()

f = open(path + "/nodelist")

args = raw_input().split()

partition_name = ""
topology_graph = 0
number_of_nodes_for_run = 0
i = 0
for i in xrange(len(args)):
        current_arg = args[i]
        if current_arg.startswith("partition="):
            partition_name = current_arg[len("partition="):]
        elif current_arg == "-g" or current_arg == "--graph":
            topology_graph = 1
        elif current_arg == "-n":
            number_of_nodes_for_run = int(args[i + 1]) 
        elif current_arg.startswith("--num=") or current_arg.startswith("--number="):
            number_of_nodes_for_run = int(current_arg[str(current_arg).index("=") + 1:])
        
nodelist = f.readlines()
f.close()
#del(nodelist[0])

cluster_info = ClusterInfo(nodelist[1:])

all_nodes_sorted = cluster_info.get_partition_nodes(partition_name)

nodes_in_partition_file = open(path + "/nodes",'w')

for i in xrange(len(all_nodes_sorted)):
    nodes_in_partition_file.write(all_nodes_sorted[i] + \
                                   (',' if i != len(all_nodes_sorted) - 1 else '\n'))
    
nodes_in_partition_file.close()

nodes_in_partition_file = open(path + "/nodes",'rw')

nodes = nodes_in_partition_file.readline().strip().split(",")

i = 0
offset_i = 0

while i < len(nodes):
    offset_j = offset_i
    j = i + number_of_nodes_for_run / 2
    nodefile = open(path + "/nodefile",'w')
    m = i + offset_i
    currnodes1 = ""
    while m < i + number_of_nodes_for_run / 2 + offset_i:
        done = False
        if m > len(nodes) - 1:
            break
        for p in cluster_info.get_partition_list(partition_name):
            if nodes[m] in p.get_all_nodes() and \
            (p.state == "alloc" or p.state == "idle"):
                currnodes1 += nodes[m] + \
                (',' if nodes[m] != \
                nodes[min(i + number_of_nodes_for_run / 2 + offset_i - 1, len(nodes) - 1)] \
                else '')
                done = True
                break
        if not done:
            offset_i += 1
        m += 1
    while j +offset_j < len(nodes):
        nodefile = open(path + "/nodefile",'w')
        nodefile.write(currnodes1)
        offset_j = max(offset_j, offset_i)
        k = j + offset_j
        while k < j + number_of_nodes_for_run / 2 + offset_j:
            if k > len(nodes) - 1:
                break
            done = False
            for p in cluster_info.get_partition_list(partition_name):
                if nodes[k] in p.get_all_nodes() and \
                (p.state == "alloc" or p.state == "idle"):
                    nodefile.write(',' + nodes[k])
                    done = True
                    break
            if not done:
                offset_j += 1
            k += 1
        nodefile.write('\n')
        nodefile.close()
        print "sbatch -N8 --nodefile=nodefile ompi network_tests2"
        f = open(path + "/res/netwtest" + str(i) + str(j),'w')
        nodefile = open(path + "/nodefile",'r')
        f.writelines(nodefile.readline())
        f.close()
        nodefile.close()
        j += number_of_nodes_for_run / 2
    i += number_of_nodes_for_run / 2

if topology_graph:
    DotGraph(open(path + "/nodes").readline()).print_graph()
        
del_pyc()


    

