import os
def CurrentFolderNameReturner(Base = False,Fullname = False):
    if Base:
        if Fullname:
            return os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(os.path.abspath(__file__)).split("\\",-2)[-1]
    if Fullname:
        return os.path.dirname(os.path.abspath(__file__))
    
    return os.path.dirname(os.path.abspath(__file__)).split("\\",-1)[-1]

print(CurrentFolderNameReturner(Base=True))