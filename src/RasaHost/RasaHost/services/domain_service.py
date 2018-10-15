import os
from RasaHost import host

class DomainService(object):
    
    domain_path = host.domain_path

    def get_text(self):
        with open(self.domain_path, "r") as f:
            return f.read()

    def update_text(self, text):
        with open(self.domain_path, "w") as f:
            f.write(text)
        pass
