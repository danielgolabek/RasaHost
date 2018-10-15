import os
from RasaHost import host

class StoriesService(object):
    
    stories_path = host.stories_path
    
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
