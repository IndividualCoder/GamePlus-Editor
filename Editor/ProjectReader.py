import json
import os

def ProjectReader(Path: str,ReturnConfig = False):
    if not os.path.exists(Path):
        raise FileNotFoundError("Given path does not exists")

    files = GetTotalFiles(Path,ReturnName=True)
    worldItems = None
    worldItemChanges = None
    UdFunc = None
    UdVars = None
    UdSrc = None
    # WindowConfig = None

    # TempPath = Path.split("\\",-1)[-1]
    Path.replace("\\","/")
    Path.replace("Editor","")
    for i in range(len(files)):
        with open(f"{Path}/{files[i]}","r") as CurrentFile:
            if files[i] == "User defined functions.txt":
                UdFunc = json.load(CurrentFile)
            elif files[i] == "User defined vars.txt":
                UdVars = json.load(CurrentFile)
            elif files[i] == "User defined src.txt":
                UdSrc = json.load(CurrentFile)
            elif files[i] == "World itmes.txt":
                worldItems = json.load(CurrentFile)
            elif files[i] == "World items changes.txt":
                worldItemChanges = json.load(CurrentFile)
            if ReturnConfig:
                if files[i] == "Window config.txt":
                    WindowConfig = json.load(CurrentFile)

    print(f"worldItems: {str(worldItems)}")
    print(f"FUnc: {str(UdFunc)}")
    print(f"var: {str(UdVars)}")
    print(f"src: {str(UdSrc)}")
    print(f"change: {str(worldItemChanges)}")
    if ReturnConfig:
        print(f"win: {str(WindowConfig)}")
    if ReturnConfig:
        return worldItems,worldItemChanges,UdFunc,UdVars,UdSrc,WindowConfig

    return worldItems,worldItemChanges,UdFunc,UdVars,UdSrc

    # with open(f"{Path}/User defined functions.txt","w") as PdFuncFile:
    #     # for i in range(len(UdFunc)):
    #         # if not PdFunc[i].endswith(";"): PdFunc[i] += ";"
    #     json.dump(UdFunc,PdFuncFile)
    # with open(f"{Path}/User defined vars.txt","w") as UdVarFile:
    #     json.dump(UdVar,UdVarFile)



# current_file_path = os.path.abspath(__file__)

# # Get the directory name (folder) from the full path
# current_folder_name = os.path.dirname(current_file_path)
# name = current_folder_name.split("\\",-1)
# name = name[-1]

def GetTotalFiles(FolderPath,StartingValue = "",Include = "Everything",ReturnName  = False):
    if Include == "Everything":
        Include = ""
    FolderPath = FolderPath
    Files= ([i for i in os.listdir(FolderPath) if os.path.isfile(os.path.join(FolderPath, i)) and i.startswith(StartingValue) and i.endswith(Include)])
    # print(f"Number of files is': {len(Files)}")
    if ReturnName:
        return Files
    return len(Files)


# ProjectReader(Path=f"{name}/Gmme")