import os

class DomainService(object):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, "data")
    domain_dir = data_dir #os.path.join(data_dir, 'domain')
    domain_path = os.path.join(domain_dir, "domain.yml")

    def get_text(self):
        with open(self.domain_path, "r") as f:
            return f.read()

    def update_text(self, text):
        with open(self.domain_path, "w") as f:
            f.write(text)
        pass
