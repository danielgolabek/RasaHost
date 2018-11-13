import os
import re
import glob
import itertools
from RasaHost import host

class NluService(object):

    def __init__(self, *args, **kwargs):
        self.nlu_path = host.nlu_path
        if not os.path.exists(self.nlu_path):
            os.makedirs(self.nlu_path)

    def get_all(self):
        model = []
        recursivePath = os.path.join(self.nlu_path, '**/**/*.md')
        for filePath in list(set(glob.iglob(recursivePath, recursive=True))):
            fileName = os.path.basename(filePath)
            with open(filePath, "r") as f:
                text = f.read()
                model.append({
                    'name': os.path.splitext(fileName)[0],
                    'path': filePath,
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

    def get_by_path(selft, path):
        intents = selft.get_all()
        return next(iter([x for x in intents if x['path'].lower() == path.lower()]), None)

    def update(self, path, model):
        with open(path, "w") as f:
            f.write(model['text'] or '')
        newPath = os.path.join(os.path.dirname(path), model['name']  + ".md")
        os.rename(path, newPath)
        return self.get_by_path(newPath)

    def create(self, model):
        path = os.path.join(self.nlu_path, model['name']  + ".md")
        with open(path, "w") as f:
            f.write(model['text'] or '')
        return self.get_by_path(path)

    def delete(self, path):
        os.remove(path)

    def get_model(self):
        model = NluFileListModel()
        for file in self.get_all():
            model.intents.append(NluFileModel(name = file["name"], path = file["path"], text = file["text"]))
        return model

    def get_model_by_path(self, path):
        file = self.get_by_path(path)
        return NluFileModel(name = file["name"], path = file["path"], text = file["text"])


class NluFileListModel(object):
    
    def __init__(self, *args, **kwargs):
        self.intents = []

    def get_intents(self):
        return list(itertools.chain(*[x.get_intents() for x in self.intents]))

class NluFileModel(object):

    def __init__(self, *args, **kwargs):
        self.lines = []
        self.name = kwargs["name"] if "name" in kwargs else None
        self.path = kwargs["path"] if "path" in kwargs else None
        if "text" in kwargs:
            self.from_text(kwargs["text"])

    def get_intents(self):
        return [x for x in self.lines if x["type"] == "intent"]

    def from_text(self, text):
        self.text = text
        for index, text in enumerate(text.splitlines()):
            line = {"text" : text, "type" : None, "name" : None, "file" : self.name}
            self.lines.append(line)
            section_type = next(iter(re.findall("\\s*##\\s*(.*?)\s*:", text)), None)
            section_name = next(iter(re.findall("\\s*##\\s*.*\s*:(.*)", text)), None)
            if section_type and section_name:
                line["type"] = section_type
                line["name"] = section_name
                continue

        return self

    def to_text(self):
        lines = [line["text"] for line in self.lines]
        return "\n".join(lines)