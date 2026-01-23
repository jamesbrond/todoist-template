"""Tests for todoist-template flows"""
import unittest
from src.config.config import TTConfig
from src.todoist import TodoistTemplateAPI
from src.todoist_actions import QuickAddAction, TemplateAction, UndoAction


class TestFlow(unittest.TestCase):
    """Test Flow class"""

    def setUp(self):
        super().setUp()
        with open('tests/.apitoken', 'r', encoding='utf8') as file:
            self.apitoken = file.read().strip()

    def test_flow_quick_add(self):
        """Test quick add flow"""
        args = ["tests/quick.txt",
                "-D", "when=tomorrow",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--dry-run",
                "--plaintext"]
        cfg = TTConfig(args)

        api = TodoistTemplateAPI(cfg)

        try:
            QuickAddAction(cfg.template).run(api)
        except Exception as e:
            self.fail(f"QuickAddAction raised an exception: {e}")

    def test_flow_template(self):
        """Test template flow"""
        args = ["tests/test.yml",
                "-D", "test_name=me,test_date=today,test_label=test",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--dry-run"]
        cfg = TTConfig(args)
        api = TodoistTemplateAPI(cfg)

        try:
            TemplateAction(cfg.template).run(api)
        except Exception as e:
            self.fail(f"TemplateAction raised an exception: {e}")

    def test_flow_undo(self):
        """Test undo flow"""
        args = ["--undo",
                "tests/test.undo",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--dry-run"]
        cfg = TTConfig(args)
        api = TodoistTemplateAPI(cfg)

        try:
            UndoAction(cfg.template).run(api)
        except Exception as e:
            self.fail(f"UndoAction raised an exception: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
