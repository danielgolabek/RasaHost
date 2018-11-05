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
            f.write(text or '')
        pass

    def get_model(self):
        return DomainModel(text = self.get_text())

    def save_model(self, model):
        self.update_text(model.to_text())

    def add_intent(self, name):
        domain = self.get_model()
        domain.add_intent(name)
        self.save_model(domain)

    def add_utter(self, name):
        domain = self.get_model()
        domain.add_utter(name)
        self.save_model(domain)

    def add_action(self, name):
        domain = self.get_model()
        domain.add_action(name)
        self.save_model(domain)
        

class DomainModel(object):

    def __init__(self, *args, **kwargs):
        self.lines = []
        if "text" in kwargs:
            self.from_text(kwargs["text"])

    def get_intents(self):
        return [x["name"] for x in self.lines if x["type"] == "intent"]

    def add_intent(self, name):
        if name in self.get_intents():
            return
        section_index = self.ensure_section("intents")
        self.lines.insert(section_index + 1, {"text" : "  - " + name, "type" : "intent", "name": name})

    def get_actions(self):
        return [x["name"] for x in self.lines if x["type"] == "action"]

    def add_action(self, name):
        if name in self.get_actions():
            return
        section_index = self.ensure_section("actions")
        self.lines.insert(section_index + 1, {"text" : "  - " + name, "type" : "action", "name": name})

    def get_utters(self):
        return [x["name"] for x in self.lines if x["type"] == "utter"]

    def add_utter(self, name):
        if name in self.get_utters():
            return
        section_index = self.ensure_section("templates")
        self.lines.insert(section_index + 1, {"text" : "  " + name + ":", "type" : "utter", "name": name})
        self.lines.insert(section_index + 2, {"text" : "  " + "- text: \"" + name + "\"", "type": None, "name": None})
        self.lines.insert(section_index + 2, {"text" : "", "type": None, "name": None})

    def ensure_section(self, name):
        section_index = None
        for index, line in enumerate(self.lines):
            if line["type"] == "section" and line["name"] == name:
                section_index = index
                break
        if section_index is None:
            self.lines.insert(0, {"text" : name + ":", "type" : "section", "name": name})
            section_index = 0
        return section_index

    def from_text(self, text):
        last_section = None
        for index, text in enumerate(text.splitlines()):
            line = {"text" : text, "type" : None, "name": None}
            self.lines.append(line)
           
            text_striped = text.strip()
            section_name = next(iter(re.findall("(.*):", text_striped)), None)
            if section_name == "intents" or section_name == "actions" or section_name == "templates":
                line["type"] = "section"
                line["name"] = section_name
                last_section = section_name
                continue
                      
            if last_section == "intents":
                if text_striped.startswith("-"):
                    name = next(iter(re.findall("\\s*-\\s*(.*)", text)), None)
                    line["name"] = name.split(':', 1)[0].strip()
                    line["type"] = "intent"
                    continue

            if last_section == "actions":
                if text_striped.startswith("-"):
                    name = next(iter(re.findall("\\s*-\\s*(.*)", text)), None)
                    line["name"] = name.split(':', 1)[0].strip()
                    line["type"] = "action"
                    continue

            if last_section == "templates":
                if text_striped.startswith("utter_"):
                    utter_name = next(iter(re.findall("(.*):", text_striped)), None)
                    line["name"] = utter_name
                    line["type"] = "utter"
                    continue
        return self;

    def to_text(self):
        lines = [line["text"] for line in self.lines]
        return "\n".join(lines)