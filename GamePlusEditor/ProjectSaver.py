import json
import os
from GamePlusEditor.ProjectSavingEncoder import ProjectSavingEncoder

def ProjectSaver(ProjectName,UdFunc,UdVar,Udsrc,WindowConfig,GameSettings,ToImport,Items,Path):
    Items = list(Items)
    # ItemChanges = []
    # for i in range(len(Items)):
    #     ItemChanges.append(Items[i].get_changes())
    # print(ItemChanges)

    if not os.path.exists(f"{Path}/{ProjectName}"):
        os.makedirs(f"{Path}/{ProjectName}")

    with open(f"{Path}/{ProjectName}/World items.txt","w") as WorldItemsFile:
        json.dump(Items,WorldItemsFile,cls=ProjectSavingEncoder)
    # with open(f"{Path}/{ProjectName}/World items changes.txt","w") as WorldItemsChangesFile:
    #     json.dump(ItemChanges,WorldItemsChangesFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/User defined functions.txt","w") as PdFuncFile:
        json.dump(UdFunc,PdFuncFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/User defined vars.txt","w") as UdVarFile:
        json.dump(UdVar,UdVarFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/User defined src.txt","w") as UdVarFile:
        json.dump(Udsrc,UdVarFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/Window config.txt","w") as WindowConfigFile:
        json.dump(WindowConfig,WindowConfigFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/Game settings.txt","w") as GameSettingsFile:
        json.dump(GameSettings,GameSettingsFile,cls=ProjectSavingEncoder)
    with open(f"{Path}/{ProjectName}/To import.txt","w") as ToImportFile:
        json.dump(ToImport,ToImportFile,cls=ProjectSavingEncoder)

