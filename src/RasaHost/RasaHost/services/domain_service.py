import os
import re
from RasaHost import host

class DomainService(object):

    def __init__(self, *args, **kwargs):
        self.domain_path = host.domain_path
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
        lastSection = None
        for index, text in enumerate(self.get_text().splitlines()):
            line = {"text" : text, "type" : None, "name": None}
            model.lines.append(line)
           
            text_striped = text.strip()
            section_name = next(iter(re.findall("(.*):", text_striped)), None)
            if section_name:
                line["type"] = "section"
                line["name"] = section_name
                lastSection = section_name
                continue
                      
            if lastSection == "intents":
                if text_striped.startswith("-"):
                    line["name"] = next(iter(re.findall("\\s*-\\s*(.*?)$|\\s|:", text)), None)
                    line["type"] = "intent"
                    continue

            if lastSection == "actions":
                if text_striped.startswith("-"):
                    line["name"] = next(iter(re.findall("\\s*-\\s*(.*?)$|\\s|:", text)), None)
                    line["type"] = "action"
                    continue

        return model

    def save_model(self, model):
        lines = [line["text"] for line in model.lines]
        text = "\n".join(lines)
        self.update_text(text)


class DomainModel(object):

    def __init__(self, *args, **kwargs):
        self.lines = []

    def get_intents(self):
        return [x["name"] for x in self.lines if x["type"] == "intent"]

    def get_actions(self):
        return [x["name"] for x in self.lines if x["type"] == "action"]

    def add_intent(self, name):
        if name in self.get_intents():
            return

        intents_section_index = None
        for index, line in enumerate(self.lines):
            if line["type"] == "section" and line["name"] == "intents":
                intents_section_index = index
                break

        if intents_section_index is None:
            self.lines.insert(0, {"text" : "intents:", "type" : "section", "name": "intents"})
            intents_section_index = 0

        self.lines.insert(intents_section_index + 1, {"text" : "  - " + name, "type" : "intent", "name": name})
