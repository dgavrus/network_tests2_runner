
class Partition:
    
    def __init__(self, name, avail, timelimit, num_of_nodes, state, nodelist):
        self.name = name
        self.avail = avail
        self.timelimit = timelimit
        self.num_of_nodes = num_of_nodes
        self.state = state
        self.nodelist = nodelist
    
    def get_all_nodes(self):
        nodes = []
        node_name_spos = 0
        node_name_fpos = -1
        bracket = 0
        node_num = ""
        i = 0
        flag = 0
        while i < len(self.nodelist):
            if bracket == 1:
                flag = 1
                if self.nodelist[i] == ',':
                    nodes.append(self.nodelist[node_name_spos:node_name_fpos] + node_num)
                    node_num = ""
                elif self.nodelist[i] == '-':
                    frange_num = ""
                    i += 1
                    while self.nodelist[i] != ',' and self.nodelist[i] != ']':
                        frange_num += self.nodelist[i]
                        i += 1
                    for x in xrange(int(node_num),int(frange_num) + 1):
                        nodes.append(self.nodelist[node_name_spos:node_name_fpos] + ('' if x > 9 else '0') + str(x))
                    if self.nodelist[i] == ']':
                        bracket = 0
                    node_num = ""
                elif self.nodelist[i] == ']':
                    bracket = 0
                    nodes.append(self.nodelist[node_name_spos:node_name_fpos] + node_num)
                    node_num = ""
                else:
                    node_num += self.nodelist[i]
            elif self.nodelist[i] == '[':
                bracket = 1
                node_name_fpos = i
            elif self.nodelist[i] == ',' or i + 1 == len(self.nodelist):
                if i + 1 == len(self.nodelist):
                    i += 1
                if flag == 0:
                    nodes.append(self.nodelist[node_name_spos:i])
                node_name_spos = i + 1
                flag = 0
            i += 1
        return nodes  
    
        
    
                
        