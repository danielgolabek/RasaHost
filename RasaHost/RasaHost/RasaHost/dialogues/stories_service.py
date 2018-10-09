import os

class StoriesService(object):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, "data")
    stories_dir = os.path.join(data_dir, 'stories')
    
    def get_all(self):
        model = []
        for fileName in os.listdir(self.stories_dir):
            with open(os.path.join(self.stories_dir, fileName), "r") as f:
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
        with open(os.path.join(self.stories_dir, name  + ".md"), "w") as f:
            f.write(model['text'])
        os.rename(os.path.join(self.stories_dir, name  + ".md"), os.path.join(self.stories_dir, model['name']  + ".md"))
        return
