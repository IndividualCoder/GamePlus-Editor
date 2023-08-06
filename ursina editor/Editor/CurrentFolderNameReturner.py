import os
def CurrentFolderNameReturner():
    return os.path.dirname(os.path.abspath(__file__)).split("\\",-1)[-1]

print(CurrentFolderNameReturner())