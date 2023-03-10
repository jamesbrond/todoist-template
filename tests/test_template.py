import unittest
from lib.config import Config
from todoist_template import get_template_content


class TestTemplate(unittest.TestCase):

    def test_template_content(self):
        with open('templates/include_template_0.yml') as file:
            template = get_template_content(file)
            self.assertTrue(template, 'Cannot get template content')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
