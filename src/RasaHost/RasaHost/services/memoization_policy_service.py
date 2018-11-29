import os
import re
import json
import zlib
import base64
import yaml
from multiprocessing import Pool
from RasaHost import host

class MemoizationPolicyService(object):

    def __init__(self, path = None, *args, **kwargs):
        self.path = path
        self.memorized_turns_path = os.path.join(self.path, 'memorized_turns.json')
        self.memorized_turns_lookups_path = os.path.join(self.path, 'memorized_turns_lookups.txt')
        pass

    def decode(self):
        if not os.path.exists(self.memorized_turns_path):
            return
        with open(self.memorized_turns_path) as f_encoded:
            memorized_turns = json.load(f_encoded)
        with open(self.memorized_turns_lookups_path, 'a+') as f_decoded:
            for lookup in memorized_turns["lookup"]:
                b64decoded = base64.b64decode(lookup)
                decompressed = zlib.decompress(bytes(b64decoded))
                text = decompressed.decode("utf-8")
                f_decoded.write(text + "\n")

    def find(self, query, last_index):
        if not os.path.exists(self.memorized_turns_lookups_path):
            return []
        lookups = []
        current_last_index = 0
        with open(self.memorized_turns_lookups_path, 'r') as f_decoded:
            for index, line in enumerate(f_decoded):
                current_last_index = index
                if current_last_index > last_index:
                   if not query or query in line:
                        lookups.append({"index": index, "line": line})
                        if len(lookups) == 100:
                            break
        return {"lookups": lookups, "last_index": last_index}

    def parse_lookup(self, lookup):
        b64decoded = base64.b64decode(lookup)
        decompressed = zlib.decompress(bytes(b64decoded))
        text = decompressed.decode("utf-8")
        return yaml.load(text)

    def parse(self):
        lookups = []
        with open(self.memorized_turns_path) as f_encoded:
            memorized_turns = json.load(f_encoded)
            with Pool() as p:
                lookups = p.map(parse_lookup, memorized_turns["lookup"])
                with open('lookups.yml', 'w') as f:
                    yaml.dump(lookups, outfile, default_flow_style=False)