import json
import os

def OpenFile(FileName: str,Folder: str,Default: None = None,MakeIfNotFound = False):
    try:
        with open(f"{Folder}/{FileName}","r") as File:
            return json.load(File)
    except FileNotFoundError:
        if not MakeIfNotFound:
            return Default
        if not os.path.exists(Folder):
            os.makedirs(Folder)
        with open(f"{Folder}/{FileName}","w") as File:
            json.dump(Default,File)
            return Default

def SaveFile(FileName: str,Folder: str,Data):
    try:
        with open(f"{Folder}/{FileName}","w") as File:
            return json.dump(Data,File)

    except FileNotFoundError:
        if not os.path.exists(Folder):
            os.makedirs(Folder)
        with open(f"{Folder}/{FileName}","w") as File:
            json.dump(Data,File)


if __name__ == "__main__":
    from OtherStuff import CurrentFolderNameReturner
    OpenFile("Hello.txt",CurrentFolderNameReturner().replace("Editor","aaa"),{"item 1": [19,True],"item 2": ["shit","helo"]},MakeIfNotFound=True)
    SaveFile('helo.txt',CurrentFolderNameReturner(),"helo\nmy")