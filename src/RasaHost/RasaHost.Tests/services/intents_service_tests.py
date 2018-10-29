import unittest
import os
from RasaHost.services import IntentsService

class IntentsServiceTests(unittest.TestCase):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    intents_path = os.path.join(current_dir, "intents")
    
    intents_service = IntentsService()
    intents_service.intents_path = intents_path

    def test_get_model_intents(self):
        model = self.intents_service.get_model()
        self.assertEqual(2, len(model))
        self.assertEqual(1, len(model[0].intents))
        self.assertEqual("goodbey", model[0].intents[0].name)
        self.assertEqual(1, len(model[1].intents))
        self.assertEqual("greet", model[1].intents[0].name)


if __name__ == '__main__':
    unittest.main()