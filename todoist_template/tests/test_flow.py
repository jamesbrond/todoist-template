"""Tests for todoist-template flows"""
import pytest
from todoist_template.config.config import TTConfig, _ttconfig_instances
from todoist_template.todoist_actions import quick_add_action, template_action
from todoist_template.__main__ import get_context
from todoist_template.todoist_api_wrapper import TodoistAPIWrapper


@pytest.fixture(autouse=True)
def _clear_singleton():
    """Clear singleton instances before each test"""
    _ttconfig_instances.clear()
    yield


@pytest.fixture
def apitoken():
    """Read the API token used by the flows"""
    with open('tests/assets/.apitoken', 'r', encoding='utf8') as file:
        return file.read().strip()


def test_flow_quick_add(apitoken):
    """Test quick add flow"""
    args = ["tests/assets/quick.txt",
            "-D", "when=tomorrow",
            "--id", "TODOIST_TEMPLATE",
            "--token", apitoken,
            "--dry-run",
            "--debug",
            "--plaintext"]
    cfg = TTConfig(args)
    with TodoistAPIWrapper(cfg) as api:
        context = get_context(cfg, api)

        try:
            quick_add_action(context)
        except Exception as e:
            pytest.fail(f"QuickAddAction raised an exception: {e}")


def test_flow_template(apitoken):
    """Test template flow"""
    args = ["tests/assets/test.yml",
            "-D", "test_name=me,test_date=today,test_label=test",
            "--id", "TODOIST_TEMPLATE",
            "--token", apitoken,
            "--debug",
            "--dry-run"]
    cfg = TTConfig(args)
    with TodoistAPIWrapper(cfg) as api:
        context = get_context(cfg, api)

        try:
            template_action(context)
        except Exception as e:
            pytest.fail(f"TemplateAction raised an exception: {e}")


# TODO undo files moved to json format: update tests/assets/test.undo file
# def test_flow_undo(apitoken):
#     """Test undo flow"""
#     args = ["--undo",
#             "tests/assets/test.undo",
#             "--id", "TODOIST_TEMPLATE",
#             "--token", apitoken,
#             "--debug",
#             "--dry-run"]
    # cfg = TTConfig(args)
    # with TodoistAPIWrapper(cfg) as api:
    #     context = get_context(cfg, api)

#     try:
#         undo_action(context)
#     except Exception as e:
#         pytest.fail(f"UndoAction raised an exception: {e}")


# ~@:-]
