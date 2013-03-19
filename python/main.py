from partition import Partition
import pwd
import os

def del_whitespace(parameters):
    for s in parameters:
        if s.isspace():
            parameters.remove(s)
username = pwd.getpwuid( os.getuid() )[ 0 ]
f = open("/home/" + username + "/nodelist")
in_string = raw_input().split(' ')
partition = ""
for split_string in in_string:
        if split_string.startswith("partition="):
            partition = split_string[len("partition="):]
            break

nodelist = f.readlines()
partitions = []
if len(partition) > 0:
    for curr_part in nodelist:
        if(curr_part.startswith(partition)):
            parameters = curr_part.split()  
            partitions.append(Partition(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5]))
            
num_of_nodes_printed = 0
num_of_nodes_real = 0
for i in xrange(len(partitions)):
    print partitions[i].name, partitions[i].state
    print partitions[i].get_all_nodes()
    num_of_nodes_printed += len(partitions[i].get_all_nodes())
    num_of_nodes_real += int(partitions[i].num_of_nodes)
    
if(num_of_nodes_printed == num_of_nodes_real):
    print "num_of_nodes_printed=",num_of_nodes_printed, "num_of_nodes_real=", num_of_nodes_real
    print "Nice job ! :)"


