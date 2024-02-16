
from GamePlusEditor.ursina import *
import json


def ProjectLoader(FileName: str, FilePath: str, FuncToEnableOnOpen):
    WorldItemsList = []
    GameSettings = []

    with open(f"{FilePath}/{FileName}/World items.txt","r") as WorldItemsFile:
        WorldItemsList = json.load(WorldItemsFile)

    # ... Other file reading code ...

    FuncToEnableOnOpen(WorldItemsList,FileName)

def SceneStateLoader(ProjectName,Path):    
    if not os.path.exists(f"{Path}/{ProjectName}"):
        return False

    with open(f"{Path}/{ProjectName}/Scene state.txt","r") as SceneStateFile:
        return json.load(SceneStateFile)

if __name__ == "__main__":
    app = Ursina()
    l = []
    # LoadProjectToScene("a","ursina editor/Current Games", l)

    # print(l)
    app.run()
