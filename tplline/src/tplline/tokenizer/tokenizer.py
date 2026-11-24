"""Tokenizer module for TPLline templates."""
import re
from pathlib import Path

# Include pattern: optional leading spaces + #! include <filename>
RE_INCLUDES = re.compile(r"(.*)#!\s*include +([A-Za-z0-9\/._-]+)[ \t]*")
# Variable pattern: {var_name} or {var_name|default_value}
RE_PLACEHOLDER = re.compile(r"{(?![fv]\[)(\w+)(?:\s*\|\s*([^}]*))?}")
# Function pattern: {f[func_name, arg1, arg2, ...]}
RE_FUNC = re.compile(r"{f\[(\w+),?(.*?)\]}")
# Comments patterns: lines starting with # (not #!) and inline comments
RE_COMMENTS = re.compile(r"(?m)^ *#[^!].*[\n\r]?", re.MULTILINE)
# Inline comments pattern: # followed by anything except !
RE_INLINE_COMMENTS = re.compile(r"\s+#(?!!).*")
# Empty lines pattern
RE_EMPTY_LINE = re.compile(r"^\s*$\r?\n", re.MULTILINE)
# Variable definition pattern: {v[var_name = value]}
RE_VARS = re.compile(r"{v\[(\w+)\s*=\s*(.*)\]}\s*")


def get_template_source_and_folder(text: str | None = None,
                                   file: Path | None = None,
                                   encoding: str = "utf-8") -> tuple[str, Path]:
    """
    Get template source and folder.
    If text is provided, return it and the current folder.
    If file is provided, read its content and return it along with its folder.
    Raise ValueError if neither is provided.
    """
    if text is not None:
        return text, Path(__file__).resolve().absolute().parent

    if file is not None and file.exists():
        return file.read_text(encoding=encoding), file.resolve().absolute().parent

    raise ValueError("TPLline tokenizer: Text or filename must be provided")


def purge_comments(text: str) -> str:
    """Remove all comments from template text; both full-line and inline comments"""
    txt = re.sub(RE_COMMENTS, '', text)
    txt = re.sub(RE_INLINE_COMMENTS, '', txt)
    txt = re.sub(RE_EMPTY_LINE, '', txt)
    return txt


def includes(text: str):
    """Yield all include matches in the text"""
    yield from RE_INCLUDES.finditer(text)


def preprocessing_includes(text: str) -> list:
    """Preprocess include statements"""
    return list(includes(text))


def tokenize_placeholders(text: str):
    """Yield all placeholder matches in the text"""
    yield from RE_PLACEHOLDER.finditer(text)


def tokenize_functions(text: str):
    """Yield all function matches in the text"""
    yield from RE_FUNC.finditer(text)


def preprocessing(text: str) -> list:
    """Preprocess variable tokens"""
    return list(tokenize_functions(text)) + list(tokenize_placeholders(text))


def tokenize_variables(text: str):
    """Yield all variable matches in the text"""
    yield from RE_VARS.finditer(text)


def preprocessing_variables(text: str) -> list:
    """Preprocess variable tokens"""
    return list(tokenize_variables(text))
