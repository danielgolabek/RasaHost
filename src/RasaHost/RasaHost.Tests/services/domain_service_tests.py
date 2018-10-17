import unittest
import os
from RasaHost.services import DomainService

class DomainServiceTests(unittest.TestCase):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    domain_path = os.path.join(current_dir, "domain.yml")
    
    domain_service = DomainService()
    domain_service.domain_path = domain_path

    def test_get_model_intents(self):
        model = self.domain_service.get_model()
        self.assertEqual(6, len(model.intents))
        self.assertEqual("greet", model.intents[0].name)
        self.assertEqual("  - greet", model.intents[0].line_text)
        self.assertEqual(1, model.intents[0].line_index)

    def test_get_model_actions(self):
        model = self.domain_service.get_model()
        self.assertEqual(5, len(model.actions))
        self.assertEqual("utter_greet", model.actions[0].name)
        self.assertEqual("- utter_greet", model.actions[0].line_text)
        self.assertEqual(11, model.actions[0].line_index)

if __name__ == '__main__':
    unittest.main()