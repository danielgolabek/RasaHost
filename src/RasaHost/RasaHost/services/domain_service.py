import os
import re
from RasaHost import host

class DomainService(object):
    
    domain_path = host.domain_path

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.domain_path):
            if not os.path.exists(os.path.dirname(self.domain_path)):
                os.makedirs(os.path.dirname(self.domain_path))
            if not os.path.exists(self.domain_path):
                with open(self.domain_path, "w") as f:
                    f.write('')

    def get_text(self):
        with open(self.domain_path, "r") as f:
            return f.read()

    def update_text(self, text):
        with open(self.domain_path, "w") as f:
            f.write(text)
        pass

    def get_model(self):
        model = DomainModel()
        in_intents_section = False
        in_actions_section = False
        for index, line in enumerate(self.get_text().splitlines()):
            line_striped = line.strip()
           
            if line_striped == "intents:":
                in_intents_section = True
                continue
            if in_intents_section:
                if line_striped.startswith("-"):
                    model.intents.append(DomainIntnetModel(
                        line_text=line, 
                        line_index=index, 
                        name=next(iter(re.findall("\\s*-\\s*(.*?)$|\\s|:", line)), None)
                    ))
                    continue
                elif line:
                    in_intents_section = False

            if line_striped == "actions:":
                in_actions_section = True
                continue
            if in_actions_section:
                if line_striped.startswith("-"):
                    model.actions.append(DomainActionModel(
                        line_text=line, 
                        line_index=index, 
                        name=next(iter(re.findall("\\s*-\\s*(.*?)$|\\s|:", line)), None)
                    ))
                    continue
                elif line:
                    in_actions_section = False
        return model

class DomainIntnetModel(object):
    name = None
    line_text = None
    line_index = None
    def __init__(self, name = None, line_text = None, line_index = None):
        self.name = name
        self.line_text = line_text
        self.line_index = line_index


class DomainActionModel(object):
    name = None
    line_text = None
    line_index = None
    def __init__(self, name = None, line_text = None, line_index = None):
        self.name = name
        self.line_text = line_text
        self.line_index = line_index


class DomainModel(object):
    intents = [] 
    actions = []
