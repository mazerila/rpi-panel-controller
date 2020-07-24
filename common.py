#
# Common functionalities required in the project
#

def getboolean(val:str):
    if (val.lower() == 'yes' or val.lower() == 'true' 
        or val.lower() == 'on' or val.lower() == '1' ):
        return True
    return False
