import json
import os
from GamePlusEditor.ProjectSavingEncoder import ProjectSavingEncoder

def ProjectSaver(ProjectName,UdFunc,UdVar,Udsrc,WindowConfig,GameSettings,ToImport,Items,Path,SaveOnlyIfProjectAlreayExists = False):
    Items = list(Items)

    if not os.path.exists(f"{Path}/{ProjectName}") and not SaveOnlyIfProjectAlreayExists:
        os.makedirs(f"{Path}/{ProjectName}")

    elif not os.path.exists(f"{Path}/{ProjectName}") and SaveOnlyIfProjectAlreayExists:
        return False

    with open(f"{Path}/{ProjectName}/World items.txt","w") as WorldItemsFile:
        json.dump(Items,WorldItemsFile,cls=ProjectSavingEncoder)

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

def SceneStateSaver(ProjectName,Path,SceneState):    
    if not os.path.exists(f"{Path}/{ProjectName}"):
        return False

    with open(f"{Path}//{ProjectName}//Scene state.txt","w") as SceneStateFile:
        json.dump(SceneState,SceneStateFile,cls = ProjectSavingEncoder)

    return True