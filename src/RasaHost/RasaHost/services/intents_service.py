import os
import re
from RasaHost import host

class IntentsService(object):
    
    intents_path = host.intents_path

    def get_all(self):
        model = []
        for fileName in os.listdir(self.intents_path):
            with open(os.path.join(self.intents_path, fileName), "r") as f:
                text = f.read()
                model.append({
                    'name': os.path.splitext(fileName)[0],
                    'text': text
                })
        return model;

    def find_all(self, q):
        q = q.lower()
        intents = self.get_all()
        return [x for x in intents if q in x['name'].lower() or q in x['text'].lower()]

    def get_by_name(selft, name):
        intents = selft.get_all()
        return next(iter([x for x in intents if x['name'].lower() == name.lower()]), None)

    def update(self, name, model):
        with open(os.path.join(self.intents_path, name  + ".md"), "w") as f:
            f.write(model['text'])
        os.rename(os.path.join(self.intents_path, name  + ".md"), os.path.join(self.intents_path, model['name']  + ".md"))
        return

    def delete(self, name):
        os.remove(os.path.join(self.intents_path, name  + ".md"))

    def get_model(self):
        model = []
        for file in self.get_all():
            fileModel = FileModel(name = file["name"])
            for index, line in enumerate(file["text"].splitlines()):
                section_type = next(iter(re.findall("\\s*##\\s*(.*?)\s*:", line)), None)
                section_name = next(iter(re.findall("\\s*##\\s*.*\s*:(.*)", line)), None)
                if section_type == "intent":
                    intent = IntnetModel(name = section_name, line_text = line, line_index = index)
                    fileModel.intents.append(intent)
                    continue
            model.append(fileModel)
        return model

class FileModel(object):
    name = None
    intents = [] 
    def __init__(self, name = None):
        self.name = name
        self.intents = [] 

class IntnetModel(object):
    name = None
    line_text = None
    line_index = None
    lines = []
    def __init__(self, name = None, line_text = None, line_index = None):
        self.name = name
        self.line_text = line_text
        self.line_index = line_index
        self.lines = []

class IntnetLineModel(object):
    line_text = None
    line_index = None
    def __init__(self, line_text = None, line_index = None):
        self.line_text = line_text
        self.line_index = line_index