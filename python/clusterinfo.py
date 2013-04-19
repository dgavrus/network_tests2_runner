
class ClusterInfo:
    
    def __init__(self, sinfo_out):
        self.__sinfo = sinfo_out
        
    def get_partition(self, partition):
        names = self.__get_partition_names()
        if not (partition in names):
            return -1
        if partition == "all":
            pass #TODO!!!
        
    def __get_partition_names(self):
        partition_names = []
        for partition in self.__sinfo:
            name = self.__del_end_star_symbol(partition.split()[0])
            partition_names.append(name)
                
        return partition_names
        
    def __parse_sinfo(self, name):
        for partition in self.__sinfo:
            current_name = self.__del_end_star_symbol(partition.split()[0])
            if name == current_name:
                pass #TODO!!!
            
    def __del_end_star_symbol(self, s):
        if s.endswith("*"):
            s = s[:len(s) - 1]
        return s
        
            
    
            
        
        