import os
import re
import itertools
from RasaHost import host

class NluService(object):

    def __init__(self, *args, **kwargs):
        self.nlu_path = host.nlu_path
        if not os.path.exists(self.nlu_path):
            os.makedirs(self.nlu_path)

    def get_all(self):
        model = []
        for fileName in os.listdir(self.nlu_path):
            with open(os.path.join(self.nlu_path, fileName), "r") as f:
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
        with open(os.path.join(self.nlu_path, name  + ".md"), "w") as f:
            f.write(model['text'])
        os.rename(os.path.join(self.nlu_path, name  + ".md"), os.path.join(self.nlu_path, model['name']  + ".md"))
        return

    def delete(self, name):
        os.remove(os.path.join(self.nlu_path, name  + ".md"))

    def get_model(self):
        model = NluListModel()
        for intent in self.get_all():
            model.intents.append(self.get_model_by_name(intent["name"]))
        return model

    def get_model_by_name(self, name):
        intent = self.get_by_name(name)
        model = NluModel()
        model.name = intent["name"]
        model.text = intent["text"]
            
        for index, text in enumerate(intent["text"].splitlines()):
            line = {"text" : text, "type" : None, "name" : None, "nlu" : name}
            model.lines.append(line)
            section_type = next(iter(re.findall("\\s*##\\s*(.*?)\s*:", text)), None)
            section_name = next(iter(re.findall("\\s*##\\s*.*\s*:(.*)", text)), None)
            if section_type and section_name:
                line["type"] = section_type
                line["name"] = section_name
                continue

        return model

    def analyze(self):
        domain_intents = DomainService().get_model().get_intents()
        nlu_intents = self.get_model().get_intents()
        intents_missing_in_domain = [x for x in nlu_intent if x["name"] not in domain_intents]
        return {'intents_missing_in_domain': intents_missing_in_domain}

class NluListModel(object):
    
    def __init__(self, *args, **kwargs):
        self.intents = []

    def get_intents(self):
        return list(itertools.chain(*[x.get_intents() for x in self.intents]))

class NluModel(object):

    def __init__(self, *args, **kwargs):
        self.lines = []
        self.name = None
        self.text = None

    def get_intents(self):
        return [x for x in self.lines if x["type"] == "intent"]