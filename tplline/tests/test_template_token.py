"""Tests for TemplateToken class."""
import json
import re
from pathlib import Path
import yaml
import pytest
from tplline.tokenizer.token import TemplateToken

ASSETS = Path(__file__).parent / "assets"


# ---------------------------------------------------------------------------
# Plain text
# ---------------------------------------------------------------------------

def test_render_plain_text():
    """Test that rendering a plain text template returns the original text."""
    token = TemplateToken(text="Hello World!")
    result = token.render({})
    assert result == "Hello World!"


def test_render_empty_template():
    """Test that rendering an empty template returns an empty string."""
    token = TemplateToken(text="")
    assert token.render({}) == ""


# ---------------------------------------------------------------------------
# Placeholders
# ---------------------------------------------------------------------------

def test_render_placeholder_with_variable():
    """Test that rendering a placeholder with a variable returns the variable's value."""
    token = TemplateToken(text="Hello {name|World}!")
    result = token.render({"name": "jbrond"})
    assert result == "Hello jbrond!"


def test_render_placeholder_uses_default_when_empty():
    """
    Test that rendering a placeholder uses the default value
    when the variable is not provided.
    """
    token = TemplateToken(text="Hello {name|World}!")
    result = token.render({})
    assert result == "Hello World!"


def test_render_placeholder_no_default_with_variable():
    """
    Test that rendering a placeholder with a variable
    and no default returns the variable's value.
    """
    token = TemplateToken(text="id={id}")
    assert token.render({"id": "42"}) == "id=42"


def test_render_placeholder_no_default_missing_variable():
    """
    Test that rendering a placeholder with no default
    and missing variable returns the original token.
    """
    # When the variable is absent and there is no default the source token is kept
    token = TemplateToken(text="{id}")
    assert token.render({}) == "{id}"


# ---------------------------------------------------------------------------
# Variable definitions  {v[name = value]}
# ---------------------------------------------------------------------------

def test_variable_definition_sets_and_resolves():
    """
    Test that a variable definition sets the variable
    and resolves it in subsequent placeholders.
    """
    # {v[x = src]} evaluates {src} with the given variables, then stores the result in x
    token = TemplateToken(text="{v[x = src]}{x|?}")
    assert token.render({"src": "hello"}) == "hello"


def test_variable_definition_produces_no_output_itself():
    """Test that a variable definition produces no output itself."""
    token = TemplateToken(text="{v[x = 1]}")
    assert token.render({}) == ""


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------

def test_comments_are_stripped_by_default():
    """Test that comment lines are stripped from the output by default."""
    token = TemplateToken(text="Hello\n# this is a comment\nWorld")
    assert "comment" not in token.render({})


def test_keep_comments_preserves_comment_lines():
    """Test that setting keep_comments=True preserves comment lines in the output."""
    token = TemplateToken(text="Hello\n# this is a comment\nWorld", keep_comments=True)
    assert "comment" in token.render({})


# ---------------------------------------------------------------------------
# YAML-like template
# ---------------------------------------------------------------------------

YAML_TEMPLATE = """\
name: {name|anonymous}
age: {age|0}
active: {active|true}
"""


def test_render_yaml_template_with_variables():
    """Test that rendering a YAML-like template with variables produces the expected output."""
    token = TemplateToken(text=YAML_TEMPLATE)
    result = token.render({"name": "jbrond", "age": "30", "active": "false"})
    assert result == "name: jbrond\nage: 30\nactive: false\n"
    parsed = yaml.safe_load(result)
    assert parsed == {"name": "jbrond", "age": 30, "active": False}


def test_render_yaml_template_defaults():
    """Test that rendering a YAML-like template with no variables uses the default values."""
    token = TemplateToken(text=YAML_TEMPLATE)
    result = token.render({})
    assert result == "name: anonymous\nage: 0\nactive: true\n"
    parsed = yaml.safe_load(result)
    assert parsed == {"name": "anonymous", "age": 0, "active": True}


# ---------------------------------------------------------------------------
# JSON-like template
# ---------------------------------------------------------------------------

JSON_TEMPLATE = """\
{
  "name": "{name|anonymous}",
  "age": "{age|0}"
}"""


def test_render_json_template_with_variables():
    """Test that rendering a JSON-like template with variables produces the expected output."""
    token = TemplateToken(text=JSON_TEMPLATE)
    result = token.render({"name": "jbrond", "age": "30"})
    assert '"name": "jbrond"' in result
    assert '"age": "30"' in result
    parsed = json.loads(result)
    assert parsed == {"name": "jbrond", "age": "30"}


def test_render_json_template_defaults():
    """Test that rendering a JSON-like template with no variables uses the default values."""
    token = TemplateToken(text=JSON_TEMPLATE)
    result = token.render({})
    assert '"name": "anonymous"' in result
    assert '"age": "0"' in result
    parsed = json.loads(result)
    assert parsed == {"name": "anonymous", "age": "0"}


# ---------------------------------------------------------------------------
# Function tokens – random_sequence
# ---------------------------------------------------------------------------

def test_func_random_sequence_length():
    """Test that the random_sequence function generates a string of the expected length."""
    # Each '@' becomes 1–2 digits (randint 0-10), non-'@' chars are preserved
    token = TemplateToken(text="{f[random_sequence, @@@]}")
    result = token.render({})
    assert len(result) >= 3


def test_func_random_sequence_digits_only():
    """
    Test that the random_sequence function generates a string
    containing only digits when using '@'.
    """
    token = TemplateToken(text="{f[random_sequence, @@@@@]}")
    result = token.render({})
    assert result.isdigit()


def test_func_random_sequence_preserves_non_at():
    """Test that the random_sequence function preserves non-'@' characters in the output."""
    token = TemplateToken(text="{f[random_sequence, A@B]}")
    result = token.render({})
    assert result[0] == "A"
    assert result[2] == "B"
    assert result[1].isdigit()


# ---------------------------------------------------------------------------
# Function tokens – random_string
# ---------------------------------------------------------------------------

def test_func_random_string_length():
    """Test that the random_string function generates a string of the expected length."""
    token = TemplateToken(text="{f[random_string, 8]}")
    result = token.render({})
    assert len(result) == 8


def test_func_random_string_uppercase():
    """Test that the random_string function generates an uppercase string."""
    token = TemplateToken(text="{f[random_string, 10]}")
    result = token.render({})
    assert result.isupper()


# ---------------------------------------------------------------------------
# Function tokens – random_number
# ---------------------------------------------------------------------------

def test_func_random_number_in_range():
    """Test that the random_number function generates a number within the specified range."""
    token = TemplateToken(text="{f[random_number, 5, 5]}")
    assert token.render({}) == "5"


@pytest.mark.parametrize("_", range(10))
def test_func_random_number_bounds(_):
    """Test that the random_number function generates a number within the specified bounds."""
    token = TemplateToken(text="{f[random_number, 1, 100]}")
    result = int(token.render({}))
    assert 1 <= result <= 100


# ---------------------------------------------------------------------------
# Function tokens – random_in
# ---------------------------------------------------------------------------

def test_func_random_in_single_choice():
    """Test that the random_in function returns the only choice when only one is provided."""
    token = TemplateToken(text="{f[random_in, only]}")
    assert token.render({}) == "only"


@pytest.mark.parametrize("_", range(10))
def test_func_random_in_picks_from_choices(_):
    """Test that the random_in function picks from the provided choices."""
    token = TemplateToken(text="{f[random_in, a, b, c]}")
    assert token.render({}) in ("a", "b", "c")


# ---------------------------------------------------------------------------
# Function tokens – random_date
# ---------------------------------------------------------------------------

def test_func_random_date_format():
    """Test that the random_date function generates a date in the expected format."""
    token = TemplateToken(text="{f[random_date, 2024-01-01, 2024-12-31, %Y-%m-%d]}")
    result = token.render({})
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", result)


def test_func_random_date_fixed_range():
    """Test that the random_date function returns the fixed date when the range is a single day."""
    token = TemplateToken(text="{f[random_date, 2024-06-15, 2024-06-15, %Y-%m-%d]}")
    assert token.render({}) == "2024-06-15"


# ---------------------------------------------------------------------------
# Function tokens – random_time
# ---------------------------------------------------------------------------

def test_func_random_time_format():
    """Test that the random_time function generates a time in the expected format."""
    token = TemplateToken(text="{f[random_time, %H:%M:%S]}")
    result = token.render({})
    assert re.fullmatch(r"\d{2}:\d{2}:\d{2}", result)


# ---------------------------------------------------------------------------
# Multiple tokens in one template
# ---------------------------------------------------------------------------

def test_render_mixed_tokens():
    """Test that a template with mixed placeholders and function tokens renders correctly."""
    # Combine a placeholder and a function token in a single template
    token = TemplateToken(text="Hello {name|World}! Code: {f[random_number, 7, 7]}")
    result = token.render({"name": "jbrond"})
    assert result == "Hello jbrond! Code: 7"


# ---------------------------------------------------------------------------
# line_prefix padding  (covers render lines 78-81)
# ---------------------------------------------------------------------------

def test_render_with_line_prefix_single_line():
    """Test that the line_prefix is correctly applied to a single-line template."""
    # line_prefix is prepended to the rendered output
    token = TemplateToken(text="Hello {name|World}!", line_prefix=">> ")
    assert token.render({}) == ">> Hello World!"


def test_render_with_line_prefix_multiline():
    """Test that the line_prefix is correctly applied to a multi-line template."""
    # First line gets the full prefix string; subsequent lines get equivalent spaces
    token = TemplateToken(text="line1\nline2\nline3", line_prefix=">> ")
    result = token.render({})
    lines = result.split("\n")
    assert lines[0].startswith(">> ")
    for line in lines[1:]:
        assert line.startswith("   ")  # same width as ">> "


# ---------------------------------------------------------------------------
# else branch in _compile  (covers line 107)
# ---------------------------------------------------------------------------

def test_compile_else_branch_falls_back_to_plaintext(monkeypatch):
    """Test that the else branch in _compile falls back to plain text when no regex matches."""
    # Inject a match from an unrecognised regex to force the else branch
    dummy_re = re.compile(r"HELLO")
    dummy_match = dummy_re.search("HELLO world")
    monkeypatch.setattr(
        "tplline.tokenizer.token.preprocessing_variables",
        lambda text: [dummy_match],
    )
    token = TemplateToken(text="HELLO world")
    assert token.render({}) == "HELLO world"


# ---------------------------------------------------------------------------
# File-based template – tests/assets/test.yml
# ---------------------------------------------------------------------------

def test_render_yaml_asset_file_produces_valid_yaml():
    """Test that rendering tests/assets/test.yml with variables produces valid YAML."""
    token = TemplateToken(file=ASSETS / "test.yml")
    result = token.render({
        "test_name": "my test",
        "test_date": "today",
        "test_label": "work",
    })
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, dict)
    assert "Inbox" in parsed
    tasks = parsed["Inbox"]["tasks"]
    assert any("my test" in t.get("content", "") for t in tasks)


def test_render_yaml_asset_file_uses_defaults():
    """Test that rendering tests/assets/test.yml without optional variables uses defaults."""
    token = TemplateToken(file=ASSETS / "test.yml")
    # test_date and test_label have no defaults; supply only those mandatory values
    result = token.render({"test_date": "tomorrow", "test_label": "home"})
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, dict)
    # test_name falls back to its default "me"
    tasks = parsed["Inbox"]["tasks"]
    assert any("me" in t.get("content", "") for t in tasks)
    # another_test_label falls back to its default ❤
    labels = tasks[0].get("labels", [])
    assert "❤" in labels


# ---------------------------------------------------------------------------
# File-based template – tests/assets/test2.yml
# ---------------------------------------------------------------------------

def test_render_yaml_asset_file_test2_produces_valid_yaml():
    """Test that rendering tests/assets/test2.yml with variables produces valid YAML."""
    token = TemplateToken(file=ASSETS / "test2.yml")
    result = token.render({
        "test_name": "my test",
        "test_date": "today",
        "test_label": "work",
    })
    parsed = yaml.safe_load(result)
    # test2.yml is a YAML list with 2 items
    assert isinstance(parsed, list)
    assert len(parsed) == 2
    # first item comes from the included test.yml
    assert "Inbox" in parsed[0]
    # second item is the main template body
    assert "Test project" in parsed[1]


def test_render_yaml_asset_file_test2_uses_defaults():
    """Test that rendering tests/assets/test2.yml without optional variables uses defaults."""
    token = TemplateToken(file=ASSETS / "test2.yml")
    result = token.render({"test_date": "tomorrow", "test_label": "home"})
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, list)
    # test_name falls back to "me" in both included and main content
    inbox_tasks = parsed[0]["Inbox"]["tasks"]
    assert any("me" in t.get("content", "") for t in inbox_tasks)
