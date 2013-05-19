import pwd, os

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def del_res():
    path = os.getcwd()[:os.getcwd().index(get_username()) + len(get_username())] + "/res/"
    for f in os.listdir(path):
            os.remove(os.path.join(path, f))

def del_pyc():
    for f in os.listdir(os.getcwd()):
        if f.endswith(".pyc"):
            os.remove(os.path.join(os.getcwd(), f))