# TPLline

**TPLline** is a simple, dependency-free template engine for Python. It renders
plain text (or any text-based format such as YAML, JSON, Markdown, HTML, …) from
a *template* by substituting placeholders, evaluating functions, expanding
inline variables and including other template files.

It is intentionally minimal: there is no sandbox, no expression language and no
control flow. It just resolves values line by line, which makes it a good fit
for generating configuration files, test fixtures, scaffolding or any repetitive
text where you want a few dynamic bits.

## What is a template?

A template is any piece of text that contains one or more **tokens**. When the
template is *rendered*, each token is replaced by its computed value and every
other character is copied verbatim. Tokens can be:

- **Placeholders** – substituted with a value passed at render time (or a
  default).
- **Functions** – calls to predefined Python functions that produce a value.
- **Variables** – values defined inside the template itself and reused later.
- **Includes** – other template files inlined at that position.
- **Comments** – notes stripped from the output.

A template can be provided as a string, read from a file, or read from standard
input.

## Template syntax

### Placeholders

```text
{name}
{name|default value}
```

A placeholder is written as `{variable_name}`. At render time it is replaced by
the value provided in the `variables` dictionary. An optional default value can
be supplied after a pipe (`|`); it is used when the variable is not provided.

If neither a value nor a default is available, the placeholder is left in the
output unchanged.

```python
TPLLine(text="Hello {name|World}!").render({})              # -> "Hello World!"
TPLLine(text="Hello {name|World}!").render({"name": "Ada"})  # -> "Hello Ada!"
```

### Functions

```text
{f[function_name, arg1, arg2, ...]}
```

A function token calls one of the [predefined functions](#predefined-functions)
and is replaced by its return value. Arguments are comma-separated and passed as
strings; leading/trailing whitespace around each argument is trimmed. A function
with no arguments is written as `{f[function_name]}`.

If the named function does not exist, the token is left in the output unchanged.

```text
Order: {f[random_sequence, 999@@@@@@@]}
Code:  {f[random_string, 6]}
Date:  {f[random_date, 2020-01-01, 2025-12-31, %Y-%m-%d]}
```

### Variables

```text
{v[variable_name = value]}
```

A variable definition assigns a value that can be reused by later placeholders
in the same template. The definition itself renders to an empty string (it is
removed from the output). The value may itself contain placeholders or function
calls.

```text
{v[order_id = f[random_sequence, 999@@@@@@@]]}
First reference:  {order_id}
Second reference: {order_id}
```

Both references resolve to the same generated value.

### Includes

```text
#! include path/to/file.txt
```

An include statement inlines another template file, resolved **relative to the
directory of the current template**. The included file is tokenized and rendered
with the same variables, so placeholders and functions inside it work as usual.

Any whitespace that appears **before** the `#!` marker is used as an indentation
prefix and applied to every line of the included content — handy for keeping
indentation-sensitive formats such as YAML valid.

```text
Header
#! include footer.txt
```

### Comments

Comments are removed from the rendered output (unless comment keeping is
enabled internally):

- **Full-line comments** – a line whose first non-space character is `#`
  (but *not* `#!`, which is reserved for includes).
- **Inline comments** – a `#` and everything after it on a line.
- **Empty lines** left behind after stripping comments are also removed.

```text
# This whole line is a comment and is dropped
value: 42   # this inline comment is dropped too
```

> Note: because `#!` is reserved for includes, use it only for include
> directives.

## Predefined functions

The following functions are available to `{f[...]}` tokens out of the box. They
are defined in [src/tplline/tokenizer/func.py](src/tplline/tokenizer/func.py).

| Function | Signature | Description |
| --- | --- | --- |
| `random_sequence` | `random_sequence(pattern)` | Returns `pattern` with every `@` replaced by a random digit (`0`–`10`). Example: `999@@@@@@@`. |
| `random_string` | `random_string(length)` | Returns a random uppercase string of the given `length`. |
| `random_date` | `random_date(min_date, max_date, format)` | Returns a random date between `min_date` and `max_date`. All three arguments use the same [strftime format](https://strftime.org/). |
| `random_time` | `random_time(format)` | Returns a random 24-hour time formatted with the given [strftime format](https://strftime.org/). |
| `random_in` | `random_in(value1, value2, ...)` | Returns one of the given values chosen at random. |
| `random_number` | `random_number(min, max)` | Returns a random integer between `min` and `max` (inclusive). |

## Installation

TPLline requires **Python 3.14+** and has no runtime dependencies.

Install the project (editable mode) from the repository root:

```bash
pip install -e .
```

Optional dependency groups are available for development workflows:

```bash
pip install -e .[dev]    # build tooling
pip install -e .[test]   # pytest, coverage, PyYAML
pip install -e .[lint]   # flake8, pylint
```

## Usage

```python
from tplline.tplline import TPLLine

# From a string
tpl = TPLLine(text="Hello {name|World}!")
print(tpl.render({"name": "Ada"}))        # Hello Ada!

# From a file
tpl = TPLLine.from_file("template.yml")
print(tpl.render({"test_name": "smoke"}))

# From standard input
tpl = TPLLine.from_stdin()
print(tpl.render({}))
```

`render(variables)` accepts a dictionary mapping placeholder names to their
values and returns the rendered text.

## Developing new functions

New functions become automatically available inside `{f[...]}` tokens — there is
no registry to update. The function token module imports everything from the
`func` module (`from tplline.tokenizer.func import *`), so any top-level function
defined there is callable from a template.

To add a function:

1. Open [src/tplline/tokenizer/func.py](src/tplline/tokenizer/func.py).
2. Define a top-level function. Keep in mind that **arguments arrive as
   strings**, so convert them as needed. The return value should be a string
   (convert non-string results with `str(...)`).

   ```python
   def repeat(text, count):
       """Repeat TEXT COUNT times."""
       return text * int(count)
   ```

3. Use it from a template:

   ```text
   {f[repeat, ab, 3]}   ->  ababab
   ```

Guidelines:

- Use `*args` when the number of arguments is variable (see `random_in`).
- Document the function with a clear docstring; it is the primary reference for
  users of the template.
- Return a `str`; template output is text.
- Avoid side effects — functions are meant to produce values, not mutate state.

## Project structure

```text
src/tplline/
  tplline.py                     # TPLLine public entry point
  tokenizer/
    tokenizer.py                 # regex patterns and preprocessing helpers
    template_token.py            # top-level template + variable tokens
    placeholder_token.py         # {name|default} tokens
    function_token.py            # {f[...]} tokens
    plaintext_token.py           # literal text
    abstract_token.py            # token base class
    func.py                      # predefined template functions
tests/                           # pytest suite and sample templates
```

## Running tests

```bash
pip install -e .[test]
pytest -v
```

## License

MIT © Diego Brondo
