import unittest
import os
from RasaHost import host
from RasaHost.services import AnalyzeService

class AnalyzeServiceTests(unittest.TestCase):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    host.nlu_path = os.path.join(current_dir, "nlu")
    host.domain_path = os.path.join(current_dir, "domain.yml")

    analyze_service = AnalyzeService()

    def test_intents_missing_in_domain(self):
        result = self.analyze_service.analyze()
        intents_missing_in_domain = result['intents_missing_in_domain']
        self.assertEqual(1, len(intents_missing_in_domain))
        self.assertEqual("age", intents_missing_in_domain[0]["name"])


if __name__ == '__main__':
    unittest.main()