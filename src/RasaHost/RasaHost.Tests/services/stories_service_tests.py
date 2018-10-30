import unittest
import os
from RasaHost import host
from RasaHost.services import StoriesService

class StoriesServiceTests(unittest.TestCase):
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    host.nlu_path = os.path.join(current_dir, "nlu")
    host.stories_path = os.path.join(current_dir, "stories")
    host.domain_path = os.path.join(current_dir, "domain.yml")
    
    stories_service = StoriesService()

    def test_get_stories(self):
        stories = self.stories_service.get_model().get_stories()
        self.assertEqual(2, len(stories))
        self.assertEqual("goodbye 01", stories[0]["name"])
        self.assertEqual("greet 01", stories[1]["name"])

    def test_create_default(self):
        self.stories_service.delete("test_story")
        self.stories_service.create_default("test_story")
        story = self.stories_service.get_model_by_name("test_story")
        self.assertEqual("## test_story", story.lines[0]["text"])
        self.assertEqual("*test_story", story.lines[1]["text"])
        self.assertEqual("-utter_test_story", story.lines[2]["text"])


if __name__ == '__main__':
    unittest.main()