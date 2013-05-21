from miniutils import get_username, del_pyc, del_res
from graph import DotGraph
from clusterinfo import ClusterInfo
import subprocess, os
import time
            
username = get_username()

del_res()

path = os.getcwd()[:os.getcwd().index(username) + len(username) + 1] + "_scratch/res/"

args = raw_input().split()

partition_name = ""
topology_graph = 0
number_of_nodes_for_run = 20
i = 0
tasks_per_batch = 4

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
        elif current_arg.startswith("--tasks="):
            tasks_per_batch = int(current_arg[str(current_arg).index("=") + 1:])
        elif current_arg == "-t":
            tasks_per_batch = int(args[i + 1])

f = open(path + "nodelist",'w')
subprocess.call(["sinfo"], stdout=f)
f.close()
f = open(path + "nodelist")                
nodelist = f.readlines()
f.close()
#del(nodelist[0])

cluster_info = ClusterInfo(nodelist[1:])

all_nodes_sorted = cluster_info.get_partition_nodes(partition_name)

nodes_in_partition_file = open(path + "nodes",'w')
for i in xrange(len(all_nodes_sorted)):
    nodes_in_partition_file.write(all_nodes_sorted[i] + \
                                   (',' if i != len(all_nodes_sorted) - 1 else '\n'))
nodes_in_partition_file.close()
nodes_in_partition_file = open(path + "nodes",'rw')
nodes = nodes_in_partition_file.readline().strip().split(",")
nodes_in_partition_file.close()


i = 0
offset_i = 0
nodefile_count = 0
running_tasks = 0
test = 0

while i < len(nodes):
    offset_j = offset_i
    j = i + number_of_nodes_for_run / 2
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
    while j + offset_j < len(nodes):
        nodefile = open(path + "nodefile" + str(nodefile_count + 1) ,'w')
        nodefile_count += 1
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
        if nodefile_count == tasks_per_batch or i + offset_i >= len(nodes) - number_of_nodes_for_run:
            for nodefile_for_run in os.listdir(path):
                if nodefile_for_run.startswith("nodefile"):
                    current_nodefile = open(path + nodefile_for_run)
                    running_nodelist = current_nodefile.readline().strip()
                    subprocess.Popen("sbatch -N" + str(min(number_of_nodes_for_run,len(nodelist.strip().split(",")))) + \
                                            " -p " + partition_name + \
                                            " --nodelist=" + running_nodelist + \
                                            " ompi " + path[:-4] + "ntest/" + "network_test2 -f " + \
                                            path + "ntest" + str(test) + " -b 0 -e 1000", shell=True)
                    #print "sbatch -N" + str(number_of_nodes_for_run) + \
                    #                         " --nodefile=" + nodefile_for_run + \
                    #                         " ompi network_tests2"
                    os.remove(path + nodefile_for_run)
            while nodefile_count == tasks_per_batch:
                time.sleep(60 * 30)
                
                f = open(path + "nodelist",'w')
                subprocess.call(["sinfo"], stdout=f)                 
                f.close()               
                f = open(path + "nodelist")                
                nodelist = f.readlines()
                f.close()       
                cluster_info = ClusterInfo(nodelist[1:])
                all_nodes_sorted = cluster_info.get_partition_nodes(partition_name)
                nodes_in_partition_file = open(path + "nodes",'w')
                for i in xrange(len(all_nodes_sorted)):
                    nodes_in_partition_file.write(all_nodes_sorted[i] + \
                                                   (',' if i != len(all_nodes_sorted) - 1 else '\n'))
                nodes_in_partition_file.close()
                nodes_in_partition_file = open(path + "nodes",'rw')
                nodes = nodes_in_partition_file.readline().strip().split(",")
                nodes_in_partition_file.close()
                squeue = subprocess.Popen("squeue | grep " + username, stdout = subprocess.PIPE, shell = True).communicate()[0]
                tasks_now = squeue.count(username)
                if tasks_now < tasks_per_batch:
                    nodefile_count = tasks_now
                    break
        j += number_of_nodes_for_run / 2
    i += number_of_nodes_for_run / 2

if topology_graph:
    DotGraph(open(path + "nodes").readline()).print_graph()
        
del_pyc()


    

