from partition import Partition

class ClusterInfo:
    
    def __init__(self, sinfo_out):
        self.__sinfo = sinfo_out        
        
    def __get_partition_parts(self, name):
        names = self.__get_partition_names()
        if not (name in names) and name != "all":
            return -1
        return self.__parse_sinfo(name)
        
    def get_partition_list(self, name):
        p = self.__get_partition_parts(name)
        partition = []
        for current_partition in p:
            parameters = current_partition.split()
            partition.append(Partition(parameters[0],parameters[1], \
                                        parameters[2],parameters[3], \
                                        parameters[4],parameters[5]))
        return partition
        
    def get_partition_nodes(self, name):
        all_nodes = []
        partitions = self.get_partition_list(name)
        for p in partitions:
            nodes = p.get_all_nodes()
            for node in nodes:
                if all_nodes.count(node) == 0:
                    all_nodes.append(node)
        all_nodes.sort(cmp=None, key=None, reverse=False)
        return all_nodes

        
    def __get_partition_names(self):
        partition_names = []
        for partition in self.__sinfo:
            name = self.__del_end_star_symbol(partition.split()[0])
            partition_names.append(name)        
        return partition_names
        
    def __parse_sinfo(self, name):
        result = []
        for partition in self.__sinfo:
            current_name = self.__del_end_star_symbol(partition.split()[0])
            if name == "all" or name == current_name:
                result.append(partition)
        return result
                
    def __del_end_star_symbol(self, s):
        if s.endswith("*"):
            s = s[:len(s) - 1]
        return s
        
            
    
            
        
        