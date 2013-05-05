import pwd, os, re

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def del_pyc():
    for f in os.listdir(os.getcwd()):
        if f.endswith(".pyc"):
            os.remove(os.path.join(os.getcwd(), f))