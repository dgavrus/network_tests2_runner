
class ClusterInfo:
    
    def __init__(self, sinfo_out):
        self.__sinfo = sinfo_out
        
    def get_partition(self, name):
        names = self.__get_partition_names()
        if not (name in names) and name != "all":
            return -1
        return self.__parse_sinfo(name)
        
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
        
            
    
            
        
        