import unittest
import os
from RasaHost import host
from RasaHost.services import NluService

class NluServiceTests(unittest.TestCase):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    host.nlu_path = os.path.join(current_dir, "nlu")
    host.domain_path = os.path.join(current_dir, "domain.yml")
    
    nlu_service = NluService()

    def test_get_intents(self):
        intents_sections = self.nlu_service.get_model().get_intents()
        self.assertEqual(3, len(intents_sections))
        self.assertEqual("age", intents_sections[0]["name"])
        self.assertEqual("goodbye", intents_sections[1]["name"])
        self.assertEqual("greet", intents_sections[2]["name"])




if __name__ == '__main__':
    unittest.main()