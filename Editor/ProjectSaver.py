import json
import os

def ProjectSaver(ProjectName,UdFunc,UdVar,Udsrc,WindowConfig,GameSettings,Items,Path):
    Items = list(Items)
    ItemChanges = []
    for i in range(len(Items)):
        ItemChanges.append(Items[i].get_changes())
    # print(ItemChanges)
    if not os.path.exists(f"{Path}/{ProjectName}"):
        os.makedirs(f"{Path}/{ProjectName}")
    # print(Path)
    # print("saved")
    # Path = "c:/Users/Me/GG/Esd/Current Games/Test game 1"
    # ProjectName = "TestGame1"
    # print(Items)
    # NewItems = []
    # for i in range(len(Items)):
    #     print(Items[i])
    # NewItems = (str(Items))

    Items = str(Items)
    # NewItems = []
    # for i in range(len(ItemChanges)):
        # NewItems.append(str(ItemChanges[i]))
    ItemChanges = str(ItemChanges)
    print(f"{Path}/{ProjectName}")
    with open(f"{Path}/{ProjectName}/World items.txt","w") as WorldItemsFile:
        json.dump(Items,WorldItemsFile)
    with open(f"{Path}/{ProjectName}/World items changes.txt","w") as WorldItemsChangesFile:
        json.dump(ItemChanges,WorldItemsChangesFile)
    with open(f"{Path}/{ProjectName}/User defined functions.txt","w") as PdFuncFile:
        json.dump(UdFunc,PdFuncFile)
    with open(f"{Path}/{ProjectName}/User defined vars.txt","w") as UdVarFile:
        json.dump(UdVar,UdVarFile)
    with open(f"{Path}/{ProjectName}/User defined src.txt","w") as UdVarFile:
        json.dump(Udsrc,UdVarFile)
    with open(f"{Path}/{ProjectName}/Window config.txt","w") as WindowConfigFile:
        json.dump(WindowConfig,WindowConfigFile)
    with open(f"{Path}/{ProjectName}/Game settings.txt","w") as GameSettingsFile:
        json.dump(GameSettings,GameSettingsFile)


# from ursina import *
# # app  = Ursina()
# e = Entity(model = "cube")
# e.position = (0,0,3)
# e.rotate((0,20,1))
# f = Entity(model = "icosphere")
# f.rotation  = (0,10,2)
# j = Button(text = "text",on_click = Func(print,"hello"))
# j.on_click = Func(print,"bue")
# j.get_changes


# # app.run()
# # Get the full path of the current Python script
# current_file_path = os.path.abspath(__file__)

# # Get the directory name (folder) from the full path
# current_folder_name = os.path.dirname(current_file_path)
# name = current_folder_name.split("\\",-1)
# name = name[-1]
# # print("Current folder name:", name)
# pdfucn = '''
# def helo(self):
#     print("my name is ptinc{current_folder_name}")
# '''

# pdvar = '''
# i = "12";for i in range(len(['asdf',"adf"])): print(i)

# '''
# pdSrc = "print('helo')"
# # ProjectSaver(pdfucn,pdvar,pdSrc,["window.fullscreen = False","window.fps_counter.disable()"],[e,f,j],Path=f"{name}/Gme")
# # if "hello " == "hello " | "B" == "B":
#     # print("es")
