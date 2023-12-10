import json
import os
import tkinter
from tkinter import filedialog

def OpenFile(FileName: str,Folder: str,Default: None = None,MakeIfNotFound = False):
    '''Function used to open a file, can be done with "with open" method but made this func to avoid boilerplate code'''
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
    '''Function used to save data in a file, can be done with "with open" method but made this func to avoid boilerplate code'''
    try:
        with open(f"{Folder}/{FileName}","w") as File:
            return json.dump(Data,File)

    except FileNotFoundError:
        if not os.path.exists(Folder):
            os.makedirs(Folder)
        with open(f"{Folder}/{FileName}","w") as File:
            json.dump(Data,File)

def Openselector(Mode = "Folder",title = "Open") -> str:
    '''The selector from which you choose your exported file destination when you export your code'''
    Root = tkinter.Tk()
    Root.withdraw() # prevents an empty tkinter window from appearing
    Path = None
    if Mode == "Folder":
        Path = filedialog.askdirectory(title = title)
    elif Mode == "File":
        Path = filedialog.askopenfile(title = title)

    Root.destroy()
    del Root
    return Path

if __name__ == "__main__":
    # from OtherStuff import CurrentFolderNameReturner
    # OpenFile("Hello.txt",CurrentFolderNameReturner().replace("Editor","aaa"),{"item 1": [19,True],"item 2": ["shit","helo"]},MakeIfNotFound=True)
    # SaveFile('helo.txt',CurrentFolderNameReturner(),"helo\nmy")
    print(f"selected file:{type(Openselector()).__name__}:")