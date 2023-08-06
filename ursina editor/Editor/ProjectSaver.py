import json
import os

def ProjectSaver(UdFunc,UdVar,Udsrc,WindowConfig,Items,Path):
    ItemChanges = []
    for i in range(len(Items)):
        ItemChanges.append(Items[i].get_changes())
    # print(ItemChanges)
    if not os.path.exists(Path):
        os.makedirs(Path)

    with open(f"{Path}/User defined functions.txt","w") as PdFuncFile:
        # for i in range(len(UdFunc)):
            # if not PdFunc[i].endswith(";"): PdFunc[i] += ";"
        json.dump(UdFunc,PdFuncFile)
    with open(f"{Path}/User defined vars.txt","w") as UdVarFile:
        json.dump(UdVar,UdVarFile)
    with open(f"{Path}/User defined src.txt","w") as UdVarFile:
        json.dump(Udsrc,UdVarFile)


from ursina import *
# app  = Ursina()
e = Entity(model = "cube")
e.position = (0,0,3)
e.rotate((0,20,1))
f = Entity(model = "icosphere")
f.rotation  = (0,10,2)
j = Button(text = "text",on_click = Func(print,"hello"))
j.on_click = Func(print,"bue")
j.get_changes


# app.run()
# Get the full path of the current Python script
current_file_path = os.path.abspath(__file__)

# Get the directory name (folder) from the full path
current_folder_name = os.path.dirname(current_file_path)
name = current_folder_name.split("\\",-1)
name = name[-1]
# print("Current folder name:", name)
pdfucn = '''
def helo(self):
    print("my name is ptinc{current_folder_name}")
'''

pdvar = '''
i = "12";for i in range(len(['asdf',"adf"])): print(i)

'''
pdSrc = "print('helo')"
ProjectSaver(pdfucn,pdvar,pdSrc,["window.fullscreen = False","window.fps_counter.disable()"],[e,f,j],Path=f"{name}/Gme")
# if "hello " == "hello " | "B" == "B":
    # print("es")
