from miniutils import get_username
import os

class DotGraph:

    def __init__(self, nodes):
        self.nodes = nodes
        self.num_main_switches = 18

    def __connect_gear(self, gear):
        connect_gear_string = ""
        for i in xrange(self.num_main_switches):
            connect_gear_string += '\t' + 'v' + str(gear) + " -- " + 'v' + str(i) + \
                " [label=\"32 Gbit/s\"]" + ';' + '\n'
        return connect_gear_string
        
    def __connect_node(self, node, gear_vertex_number, current_vertex):
        # get the gear switch vertex number 
        gear_switch_number = ((gear_vertex_number + 1) if int(str(node)[-2:]) <= 16 \
                                                    else gear_vertex_number + 2)
        ###
        return 'v' + str(gear_switch_number) + \
                " -- " + \
                'v' + str(current_vertex)
        
    def print_graph(self):
        username = get_username()
        path = os.getcwd()[:os.getcwd().index(username) + len(username)]
        f = open(path + "/vertexes.tmp",'w')
        g = open(path + "/nodes.tmp",'w')
        for i in xrange(self.num_main_switches):
            f.write('\t' + 'v' + str(i) + " [label=\"main\"]" + ';' + '\n')
        current_vertex = self.num_main_switches # current vertex number
        split_nodes = self.nodes.split(',') # get list of nodes
        
        gears = {}                          # gears dictionary
                                            # key is a string with name of gear
                                            # value is a vertex number in graph
                                               
        for node in split_nodes:            
            if not gears.has_key(str(node)[:9]):
                gears[str(node)[:9]] = current_vertex
                f.write('\t' + 'v' + str(current_vertex) + " [label=\"gear-" + node[6:9] + "\"]" + ';' + '\n')
                g.write(self.__connect_gear(current_vertex))
                g.write('\t' + 'v' + str(current_vertex) + " -- " + 'v' + str(current_vertex + 1) + " [label=\"32 Gbit/s\"]" +  ';' + '\n')
                g.write('\t' + 'v' + str(current_vertex) + " -- " + 'v' + str(current_vertex + 2) + " [label=\"32 Gbit/s\"]" + ';' + '\n')
                f.write('\t' + 'v' + str(current_vertex + 1) + " [label=\"switch1-" + node[6:9] + "\"]" + ';' + '\n')
                f.write('\t' + 'v' + str(current_vertex + 2) + " [label=\"switch2-" + node[6:9] + "\"]" + ';' + '\n')
                current_vertex += 3
            g.write('\t' + self.__connect_node(node, gears[str(node)[:9]], current_vertex) + " [label=\"32 Gbit/s\"]" + ';' + '\n')
            f.write('\t' + 'v' + str(current_vertex) + " [label=\"" + node + "\"]" + ';' + '\n')
            current_vertex += 1
        
        f.close()
        g.close()
        f = open(path + "/vertexes.tmp","r+")
        g = open(path + "/nodes.tmp","r+")
        vertexes = f.readlines()
        nodes = g.readlines()
        vertexes.sort()
        nodes.sort()
        f.close()
        g.close()
        os.remove(path + "/vertexes.tmp")
        os.remove(path + "/nodes.tmp")
        f = open(path + "/topology_graph","w")
        f.write("graph topology {" + '\n')
        f.writelines(tuple(vertexes))
        f.writelines(tuple(nodes))
        f.write('}' + '\n')
        f.close()
           
            
                
            
            
                
            
            