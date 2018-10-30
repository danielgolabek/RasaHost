import os
import re
import itertools
from RasaHost import host

class StoriesService(object):
    
    def __init__(self, *args, **kwargs):
        self.stories_path = host.stories_path
        if not os.path.exists(self.stories_path):
            os.makedirs(self.stories_path)

    def get_all(self):
        model = []
        for fileName in os.listdir(self.stories_path):
            with open(os.path.join(self.stories_path, fileName), "r") as f:
                text = f.read()
                model.append({
                    'name': os.path.splitext(fileName)[0],
                    'text': text
                })
        return model;

    def find_all(self, q):
        q = q.lower()
        stories = self.get_all()
        return [x for x in stories if q in x['name'].lower() or q in x['text'].lower()]

    def get_by_name(selft, name):
        stories = selft.get_all()
        return next(iter([x for x in stories if x['name'].lower() == name.lower()]), None)

    def update(self, name, model):
        with open(os.path.join(self.stories_path, name  + ".md"), "w") as f:
            f.write(model['text'])
        os.rename(os.path.join(self.stories_path, name  + ".md"), os.path.join(self.stories_path, model['name']  + ".md"))
        return

    def update_text(self, name, text):
        with open(os.path.join(self.stories_path, name  + ".md"), "w") as f:
            f.write(text)
        return

    def delete(self, name):
        if os.path.exists(os.path.join(self.stories_path, name  + ".md")):
            os.remove(os.path.join(self.stories_path, name  + ".md"))

    def create_default(self, name):
        story = StoriesFileModel().create_default(name)
        self.save_model(story)
        return story

    def save_model(self, model):
        if isinstance(model, StoriesFileModel):
            lines = [line["text"] for line in model.lines]
            text = "\n".join(lines)
            self.update_text(model.name, text)

    def get_model(self):
        model = StoriesFileListModel()
        for storyFile in self.get_all():
            model.stories.append(self.get_model_by_name(storyFile["name"]))
        return model

    def get_model_by_name(self, name):
        story = self.get_by_name(name)
        model = StoriesFileModel()
        model.name = story["name"]
        model.text = story["text"]
            
        for index, text in enumerate(story["text"].splitlines()):
            line = {"text" : text, "type" : None, "name" : None, "file" : name}
            model.lines.append(line)
            story_name = next(iter(re.findall("\\s*##\\s*(.*)", text)), None)
            if story_name:
                line["type"] = "story"
                line["name"] = story_name
                continue
            intent_name = next(iter(re.findall("\\s*\\*\\s*(.*)", text)), None)
            if intent_name:
                line["type"] = "intent"
                line["name"] = intent_name
                continue
            action_name = next(iter(re.findall("\\s\\-\\s*(.*)", text)), None)
            if action_name:
                line["type"] = "action"
                line["name"] = action_name
                continue
        return model


class StoriesFileListModel(object):
    
    def __init__(self, *args, **kwargs):
        self.stories = []

    def get_stories(self):
        return list(itertools.chain(*[x.get_stories() for x in self.stories]))

    def get_all_intents(self):
        return list(itertools.chain(*[x.get_all_intents() for x in self.stories]))

class StoriesFileModel(object):

    def __init__(self, *args, **kwargs):
        self.lines = []
        self.name = None
        self.text = None

    def get_stories(self):
        return [x for x in self.lines if x["type"] == "story"]

    def get_all_intents(self):
        return [x for x in self.lines if x["type"] == "intent"]

    def add_title(self, name):
        self.lines.append({"text" : "## "+ name, "type" : "story", "name" : name, "file" : self.name})
        return self

    def add_intent(self, name):
        self.lines.append({"text" : "*"+ name, "type" : "intent", "name" : name, "file" : self.name})
        return self

    def add_utter(self, name):
        self.lines.append({"text" : "-"+ name, "type" : "utter", "name" : name, "file" : self.name})
        return self

    def create_default(self, name):
        self.name = name;
        self.add_title(name)
        self.add_intent(name)
        self.add_utter("utter_" + name)
        return self