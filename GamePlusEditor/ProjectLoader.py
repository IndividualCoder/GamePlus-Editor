# from ursina import *
# import json
# def LoadProjectToScene(FileName: str, FilePath: str,wa: list):
#     WorldItemsList = []
#     GameSettings = []

#     with open(f"{FilePath}/{FileName}/World items.txt","r") as WorldItemsFile:
#         WorldItemsList = (json.load(WorldItemsFile))
#     with open(f"{FilePath}/{FileName}/Game settings.txt","r") as GameSettingsFile:
#         GameSettings = json.load(GameSettingsFile)
#     with open(f"{FilePath}/{FileName}/User defined functions.txt","r") as GameSettingsFile:
#         UdFunc = json.load(GameSettingsFile)
#     with open(f"{FilePath}/{FileName}/User defined src.txt","r") as GameSettingsFile:
#         UdSrc = json.load(GameSettingsFile)
#     with open(f"{FilePath}/{FileName}/User defined vars.txt","r") as GameSettingsFile:
#         UdVars = json.load(GameSettingsFile)

#     print(WorldItemsList)
#     for i in range(len(WorldItemsList)):
#         exec(f"{wa}.append({WorldItemsList[i]['cls']}{WorldItemsList[i]['args']})")


#     # return wa,GameSettings,UdFunc,UdSrc,UdVars
#     # print(WorldItemsList)

# if __name__ == "__main__":
#     app = Ursina()
#     LoadProjectToScene("a","Current Games",l:=[])

#     print(l)
#     app.run()

from GamePlusEditor.ursina import *
import json

def LoadProjectToScene(FileName: str, FilePath: str, FuncToEnableOnOpen):
    WorldItemsList = []
    GameSettings = []

    with open(f"{FilePath}/{FileName}/World items.txt","r") as WorldItemsFile:
        WorldItemsList = json.load(WorldItemsFile)

    # ... Other file reading code ...

    # print(WorldItemsList)
    FuncToEnableOnOpen(WorldItemsList,FileName)
    # for item in WorldItemsList:
    #     # Evaluate the class constructor as an expression and append the result to the list
    #     List.append(eval(item['cls'] + item['args']))

    # print(List)

if __name__ == "__main__":
    app = Ursina()
    l = []
    # LoadProjectToScene("a","ursina editor/Current Games", l)

    # print(l)
    app.run()
