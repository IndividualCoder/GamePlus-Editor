import json
import os
from GamePlusEditor.ursina import *
# from CurrentFolderNameReturner import CurrentFolderNameReturner

def GetRecentProjects(Path = f"TestToFindProjects/TestFolder",Exclude = "__pycache__",order = None):
    TotalFolders = GetTotalFolders(Path,Exclude=Exclude)
    ResultFile = {}
    # temp = []
    for i in range(len(TotalFolders)):
        ResultFile[f"{TotalFolders[i]}"] = (GetFileData(f"{Path}/{TotalFolders[i]}"))
        # temp.append(GetFileData(f"{Path}/{TotalFolders[i]}",File="World items.txt"))

        # print(f"{Path}/{TotalFolders[i]}")
    # print("you looking for me!",temp)
    # print(type(temp[0][0]).__name__)

    # print(ResultFile)

    if order:
        try:
            ResultFile = [(Data, ResultFile[Data]) for Data in order]
        except Exception as e:
            print(e)
    return dict(ResultFile)


def GetTotalFiles(FolderPath = f"{application.asset_folder}/ModifiedUrsinaWithExperiments",StartingValue = "",Include = "Everything",ReturnName  = False):
    if Include == "Everything":
        Include = ""
    FolderPath = FolderPath
    Files= ([i for i in os.listdir(FolderPath) if os.path.isfile(os.path.join(FolderPath, i)) and i.startswith(StartingValue) and i.endswith(Include)])
    # print(f"Number of files is': {len(Files)}")
    if ReturnName:
        return Files
    return len(Files)

def GetTotalFolders(Path  = f"{application.asset_folder}/ModifiedUrsinaWithExperiments",Exclude = "",ReturnName = True):
    FolderPath = Path  # Get the current working directory
    FolderNames = []

    try:
        if isinstance(Exclude,str):
            FolderNames = [i for i in os.listdir(FolderPath) if os.path.isdir(os.path.join(FolderPath, i)) and i != Exclude]
        elif isinstance(Exclude,list):
            FolderNames = [i for i in os.listdir(FolderPath) if os.path.isdir(os.path.join(FolderPath, i)) and i not in Exclude]
    except FileNotFoundError:
        # if Path.split("/",-1)[-2] == CurrentFolderNameReturner(True):
        #     Path = Path.split(-1)[-1]
        os.makedirs(Path)

    FolderCount = len(FolderNames)

    # print(f"Total number of folders: {FolderCount}")
    # print("Folder names:")
    # for name in FolderNames:
    #     print(name)
    if ReturnName:
        return FolderNames
    return FolderCount

def GetFileData(Path,File:str = "Game settings.txt"):
    try:
        ToReturn = None 
        with open(f"{Path}/{File}","r") as ToOpenFile:
            ToReturn = json.load(ToOpenFile)
            # print("loaded",ToReturn)
        return ToReturn
    except Exception as e:
        # print(Exception)
        print(e)
# print(GetRecentProjects(order = ["TestProject2Folder","TestProject1Folder"]))
