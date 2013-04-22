import pwd, os

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def del_pyc():
    os.remove(os.getcwd() + "/*.pyc")