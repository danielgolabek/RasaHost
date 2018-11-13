import os
import re
import glob
import itertools
from RasaHost import host

class StoriesService(object):
    
    def __init__(self, *args, **kwargs):
        self.stories_path = host.stories_path
        if not os.path.exists(self.stories_path):
            os.makedirs(self.stories_path)

    def get_all(self):
        model = []
        recursivePath = os.path.join(self.stories_path, '**/**/*.md')
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
        stories = self.get_all()
        return [x for x in stories if q in x['name'].lower() or q in x['text'].lower()]

    def get_by_name(selft, name):
        stories = selft.get_all()
        return next(iter([x for x in stories if x['name'].lower() == name.lower()]), None)

    def get_by_path(selft, path):
        stories = selft.get_all()
        return next(iter([x for x in stories if x['path'].lower() == path.lower()]), None)

    def get_text_by_name(selft, name):
        story = selft.get_by_name(name)
        if story:
            return story["text"]
        return None

    def get_text_by_path(selft, path):
        story = selft.get_by_path(path)
        if story:
            return story["text"]
        return None

    def update(self, path, model):
        with open(path, "w") as f:
            f.write(model['text'] or '')
        newPath = os.path.join(os.path.dirname(path), model['name']  + ".md")
        os.rename(path, newPath)
        return self.get_by_path(newPath)

    def create(self, model):
        path = os.path.join(self.stories_path, model['name']  + ".md")
        with open(path, "w") as f:
            f.write(model['text'] or '')
        return self.get_by_path(path)

    def update_text(self, path, text):
        with open(path, "w") as f:
            f.write(text or '')
        return

    def delete(self, name):
        if os.path.exists(os.path.join(self.stories_path, name  + ".md")):
            os.remove(os.path.join(self.stories_path, name  + ".md"))

    def save_model(self, model):
        if isinstance(model, StoriesFileModel):
            lines = [line["text"] for line in model.lines]
            text = "\n".join(lines)
            self.update_text(model.path, text)

    def get_model(self):
        model = StoriesFileListModel()
        for file in self.get_all():
            model.stories.append(StoriesFileModel(name = file["name"], path = file["path"], text = file["text"]))
        return model

    def get_model_by_path(self, path):
        file = self.get_by_path(path)
        if not file:
            return None
        return StoriesFileModel(name = file["name"], path = file["path"], text = file["text"])

    def get_model_by_name(self, name):
        path = os.path.join(self.stories_path, name  + ".md")
        return self.get_model_by_path(path)
    

    def add_story(self, intent, utter):
        story = self.get_model_by_name(intent) or StoriesFileModel(name = intent, path = os.path.join(self.stories_path, intent  + ".md"))
        story.add_story(intent, utter)
        self.save_model(story)
        return story


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
        self.name = kwargs["name"] if "name" in kwargs else None
        self.path = kwargs["path"] if "path" in kwargs else None
        if "text" in kwargs:
            self.from_text(kwargs["text"])

    def get_stories(self):
        return [x for x in self.lines if x["type"] == "story"]

    def get_all_intents(self):
        return [x for x in self.lines if x["type"] == "intent"]

    def add_empty_line(self, name):
        self.lines.append({"text" : "" + name, "type" : None, "name" : None, "file" : self.name})
        return self

    def add_title(self, name):
        self.lines.append({"text" : "## "+ name, "type" : "story", "name" : name, "file" : self.name})
        return self

    def add_intent(self, name):
        self.lines.append({"text" : "*"+ name, "type" : "intent", "name" : name, "file" : self.name})
        return self

    def add_utter(self, name):
        self.lines.append({"text" : "-"+ name, "type" : "utter", "name" : name, "file" : self.name})
        return self

    def add_story(self, intent, utter):
        if (len(self.lines) > 0):
            self.add_empty_line(intent)
        self.add_title(intent)
        self.add_intent(intent)
        self.add_utter(utter)
        return self

    def from_text(self, text):
        self.text = text
        for index, text in enumerate(text.splitlines()):
            line = {"text" : text, "type" : None, "name" : None, "file" : self.name}
            self.lines.append(line)
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

    def to_text(self):
        lines = [line["text"] for line in self.lines]
        return "\n".join(lines)