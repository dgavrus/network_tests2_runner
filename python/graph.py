from username import get_username
import os

class DotGraph:

    def __init__(self, nodes):
        self.nodes = nodes
        self.num_main_switches = 18

    def __connect_gear(self, gear):
        connect_gear_string = ""
        for i in xrange(self.num_main_switches):
            connect_gear_string += 'v' + str(gear) + " -- " + 'v' + str(i) + ';' + '\n'
        return connect_gear_string
        
    def __connect_node(self, node, gear_vertex_number, current_vertex):
        gear_switch_number = ((gear_vertex_number + 1) if int(str(node)[-2:]) <= 16 \
                                                    else gear_vertex_number + 2)
        return 'v' + str(gear_switch_number) + \
                " -- " + \
                'v' + str(current_vertex)
        
    def print_graph(self):
        f = open("/home/" + get_username() + "/vertexes.tmp",'w')
        g = open("/home/" + get_username() + "/nodes.tmp",'w')
       # f.write("graph topology {" + '\n')
        for i in xrange(self.num_main_switches):
            f.write('v' + str(i) + "[label=\"main\"]" + ';' + '\n')
        current_vertex = self.num_main_switches # current vertex number
        split_nodes = self.nodes.split(',') # get list of nodes
        
        gears = {}                          # gears dictionary
                                            # key is a string with name of gear
                                            # value is a vertex number in graph
                                               
        for node in split_nodes:            
            if not gears.has_key(str(node)[:9]):
                gears[str(node)[:9]] = current_vertex
                g.write(self.__connect_gear(current_vertex))
                g.write('v' + str(current_vertex) + " -- " + 'v' + str(current_vertex + 1) + "[label=\"32Gbit/s  \"]" +  ';' + '\n')
                g.write('v' + str(current_vertex) + " -- " + 'v' + str(current_vertex + 2) + "[label=\"32Gbit/s  \"]" + ';' + '\n')
                f.write('v' + str(current_vertex + 1) + "[label=\"" + node + "\"]" + ';' + '\n')
                f.write('v' + str(current_vertex + 2) + "[label=\"" + node + "\"]" + ';' + '\n')
                current_vertex += 3
            g.write(self.__connect_node(node, gears[str(node)[:9]], current_vertex) + "[label=\"32Gbit/s  \"]" + ';' + '\n')
            current_vertex += 1
        
       # f.write('}' + '\n')
        f.close()
        g.close()
        f = open("/home/" + get_username() + "/vertexes.tmp","r+")
        g = open("/home/" + get_username() + "/nodes.tmp","r+")
        vertexes = f.readlines()
        nodes = g.readlines()
        vertexes.sort()
        nodes.sort()
        f.close()
        g.close()
        os.remove("/home/" + get_username() + "/vertexes.tmp")
        os.remove("/home/" + get_username() + "/nodes.tmp")
        f = open("/home/" + get_username() + "/topology_graph","r+")
        f.write("graph topology {" + '\n')
        f.writelines(tuple(vertexes))
        f.writelines(tuple(nodes))
        f.write('}' + '\n')
        f.close()

        
      # Gbit/s      
            
                
            
            
                
            
            