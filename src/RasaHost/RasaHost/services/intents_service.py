import os
from RasaHost import host

class IntentsService(object):
    
    intents_path = host.intents_path

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.intents_path):
            os.makedirs(self.intents_path)

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