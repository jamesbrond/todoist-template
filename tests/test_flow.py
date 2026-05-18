"""Tests for todoist-template flows"""
import unittest
from config.config import TTConfig, _ttconfig_instances
from todoist_actions import quick_add_action, undo_action, template_action
from todoist_template import get_context


class TestFlow(unittest.TestCase):
    """Test Flow class"""

    def setUp(self):
        super().setUp()
        # Clear singleton instances for tests
        _ttconfig_instances.clear()
        with open('tests/.apitoken', 'r', encoding='utf8') as file:
            self.apitoken = file.read().strip()

    def test_flow_quick_add(self):
        """Test quick add flow"""
        args = ["tests/quick.txt",
                "-D", "when=tomorrow",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--dry-run",
                "--debug",
                "--plaintext"]
        context = get_context(TTConfig(args))

        try:
            quick_add_action(context)
        except Exception as e:
            self.fail(f"QuickAddAction raised an exception: {e}")

    def test_flow_template(self):
        """Test template flow"""
        args = ["tests/test.yml",
                "-D", "test_name=me,test_date=today,test_label=test",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--debug",
                "--dry-run"]
        context = get_context(TTConfig(args))

        try:
            template_action(context)
        except Exception as e:
            self.fail(f"TemplateAction raised an exception: {e}")

    def test_flow_undo(self):
        """Test undo flow"""
        args = ["--undo",
                "tests/test.undo",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--debug",
                "--dry-run"]
        context = get_context(TTConfig(args))

        try:
            undo_action(context)
        except Exception as e:
            self.fail(f"UndoAction raised an exception: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
