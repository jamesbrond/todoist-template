"""Tests for todoist-template flows"""
import unittest
from config.config import TTConfig, _ttconfig_instances
from todoist import TodoistTemplateAPI
from todoist_actions import TemplateContext, quick_add_action, undo_action, template_action


class TestFlow(unittest.TestCase):
    """Test Flow class"""

    def setUp(self):
        super().setUp()
        # Clear singleton instances for tests
        _ttconfig_instances.clear()
        with open('tests/.apitoken', 'r', encoding='utf8') as file:
            self.apitoken = file.read().strip()

    def get_context(self, args: list[str]) -> TemplateContext:
        """Get TemplateContext from args"""
        cfg = TTConfig(args)
        context: TemplateContext = TemplateContext(
            api=TodoistTemplateAPI(cfg),
            template=cfg.template,
            variables=cfg.variables,
            is_dry_run=cfg.dry_run,
            is_update_tasks=cfg.is_update
        )
        return context

    def test_flow_quick_add(self):
        """Test quick add flow"""
        args = ["tests/quick.txt",
                "-D", "when=tomorrow",
                "--id", "TODOIST_TEMPLATE",
                "--token", self.apitoken,
                "--dry-run",
                "--debug",
                "--plaintext"]
        context = self.get_context(args)

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
        context = self.get_context(args)

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
        context = self.get_context(args)

        try:
            undo_action(context)
        except Exception as e:
            self.fail(f"UndoAction raised an exception: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
