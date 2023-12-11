from json import JSONEncoder
from GamePlusEditor.ursina import Entity

class ProjectSavingEncoder(JSONEncoder):
    def default(self, o):
        try:
            return o.__dict__()
        except:
            # return JSONEncoder.default(self=o=o)
            return JSONEncoder.default(JSONEncoder,o)
