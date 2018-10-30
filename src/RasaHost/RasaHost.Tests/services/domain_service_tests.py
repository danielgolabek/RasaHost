import unittest
import os
from RasaHost import host
from RasaHost.services import DomainService

class DomainServiceTests(unittest.TestCase):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    host.nlu_path = os.path.join(current_dir, "nlu")
    host.domain_path = os.path.join(current_dir, "domain.yml")
    
    domain_service = DomainService()

    def test_get_model_intents(self):
        model = self.domain_service.get_model()
        intents = model.get_intents()

        self.assertEqual(6, len(intents))
        self.assertEqual("greet", intents[0])
        self.assertEqual("goodbye", intents[1])

    def test_get_model_actions(self):
        model = self.domain_service.get_model()
        actions = model.get_actions()

        self.assertEqual(5, len(actions))
        self.assertEqual("utter_greet", actions[0])
        self.assertEqual("utter_cheer_up", actions[1])

    def test_add_intent_to_existing(self):
        model = self.domain_service.get_model()
        self.assertTrue("new intent" not in model.get_intents())
        model.add_intent("new intent")
        self.assertTrue("new intent" in model.get_intents())

    def test_add_intent_to_new(self):
        model = self.domain_service.get_model()
        model.lines = []
        self.assertTrue("new intent" not in model.get_intents())
        model.add_intent("new intent")
        self.assertTrue("new intent" in model.get_intents())
        self.assertEqual("intents",  model.lines[0]["name"])
        self.assertEqual("section", model.lines[0]["type"])

if __name__ == '__main__':
    unittest.main()