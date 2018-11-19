import os
import re
import glob
import re
import itertools
from RasaHost import host

class QueryParser(object):
    
    def __init__(self, *args, **kwargs):
        pass

    def parse(self, query):
        words = query.split()
        parsed_query = []
        for word in words:
            tokens = word.split(":",1)
            if len(tokens) == 2:
                parsed_query.append({tokens[0]: tokens[1]})
            else:
                parsed_query.append(word);
        return parsed_query;

   