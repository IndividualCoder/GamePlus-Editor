import json
import os
from ursina import *

def GetRecentProjects(Path = f"{application.asset_folder}/ModifiedUrsinaWithExperiments",Exclude = "__pycache__"):
    ProjectFiles = GetTotalFiles(ReturnName=True,Include=".py")
    print(ProjectFiles[0])
    FolderNameList = []
    for i in range(ProjectFiles[1]):
        with open(f"{Path}/{ProjectFiles[0][i]}","r") as File:
            FolderNameList.append([File.name])
            # print(File)
            print(FolderNameList)
        # with open("CurrentProjects/")
        pass

def GetTotalFiles(FolderPath = f"{application.asset_folder}/ModifiedUrsinaWithExperiments",StartingValue = "",Include = "Everything",ReturnName  = False):
    if Include == "Everything":
        Include = ""
    FolderPath = FolderPath
    Files= ([i for i in os.listdir(FolderPath) if os.path.isfile(os.path.join(FolderPath, i)) and i.startswith(StartingValue) and i.endswith(Include)])
    print(f"Number of files is': {len(Files)}")
    if ReturnName:
        return [Files,len(Files)]
    return len(Files)
# GetTotalFiles()

def GetTotalFolders(Path  = f"{application.asset_folder}/ModifiedUrsinaWithExperiments",Exclude = "",ReturnName = True):
    FolderPath = Path  # Get the current working directory
    if isinstance(Exclude,str):
        FolderNames = [i for i in os.listdir(FolderPath) if os.path.isdir(os.path.join(FolderPath, i)) and i != Exclude]
    elif isinstance(Exclude,list):
        FolderNames = [i for i in os.listdir(FolderPath) if os.path.isdir(os.path.join(FolderPath, i)) and i not in Exclude]

    FolderCount = len(FolderNames)

    print(f"Total number of folders: {FolderCount}")
    print("Folder names:")
    for name in FolderNames:
        print(name)
    if ReturnName:
        return [FolderNames,FolderCount]
    return FolderCount


# GetTotalFolders(Exclude=["__pycache__"])
GetRecentProjects()
