import os
import re
import itertools
from RasaHost import host
from RasaHost.services import DomainService, NluService, StoriesService

class AnalyzeService(object):
    
    def analyze(self):
        domain_intents = DomainService().get_model().get_intents()
        
        nlu_intents = NluService().get_model().get_intents()
        intents_missing_in_domain = [x for x in nlu_intents if x["name"] not in domain_intents]

        stories_intents = [x["name"] for x in StoriesService().get_model().get_all_intents()]
        intents_missing_in_stories = [x for x in nlu_intents if x["name"] not in stories_intents]

        return {
            'intents_missing_in_domain': intents_missing_in_domain,
            'intents_missing_in_stories': intents_missing_in_stories
            }
