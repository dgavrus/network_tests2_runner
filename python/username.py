import pwd, os

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]