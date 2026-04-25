"""wordwrap — ANSI-aware paragraph wrap, fill, and shorten."""
from __future__ import annotations

import re
import unicodedata
from typing import List

__all__ = ["WrapError", "fill", "shorten", "strip_ansi", "visible_width", "wrap"]
__version__ = "0.1.0"

_ANSI = re.compile(r"\x1b\[[0-9;:?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


class WrapError(ValueError):
    """Raised on invalid input."""


def strip_ansi(text: str) -> str:
    """Remove CSI / OSC / SGR escape sequences from text."""
    if not isinstance(text, str):
        raise WrapError(f"text must be str, got {type(text).__name__}")
    return _ANSI.sub("", text)


def visible_width(text: str) -> int:
    """Measure printed width: ANSI ignored, CJK as 2, combining as 0."""
    if not isinstance(text, str):
        raise WrapError(f"text must be str, got {type(text).__name__}")
    plain = strip_ansi(text)
    width = 0
    for ch in plain:
        if unicodedata.combining(ch):
            continue
        ea = unicodedata.east_asian_width(ch)
        width += 2 if ea in ("W", "F") else 1
    return width


def _validate_width(width: object) -> int:
    if isinstance(width, bool) or not isinstance(width, int):
        raise WrapError("width must be a positive int")
    if width <= 0:
        raise WrapError("width must be positive")
    return width


def wrap(
    text: str,
    width: int,
    *,
    initial_indent: str = "",
    subsequent_indent: str = "",
    break_long_words: bool = True,
    tabsize: int = 8,
    drop_whitespace: bool = True,
) -> List[str]:
    """Wrap text into a list of lines no wider than `width` columns."""
    if not isinstance(text, str):
        raise WrapError(f"text must be str, got {type(text).__name__}")
    width = _validate_width(width)
    if not isinstance(initial_indent, str) or not isinstance(subsequent_indent, str):
        raise WrapError("indents must be strings")
    if not isinstance(tabsize, int) or tabsize < 0:
        raise WrapError("tabsize must be a non-negative int")
    expanded = text.expandtabs(tabsize) if tabsize > 0 else text
    plain = strip_ansi(expanded)
    if not plain.strip() and drop_whitespace:
        return []
    words = plain.split()
    lines: List[str] = []
    indent = initial_indent
    cur: List[str] = []
    cur_width = visible_width(indent)
    for word in words:
        wlen = visible_width(word)
        space = 1 if cur else 0
        if cur_width + space + wlen <= width:
            cur.append(word)
            cur_width += space + wlen
        elif break_long_words and wlen + visible_width(indent) > width:
            if cur:
                lines.append(indent + " ".join(cur))
                indent = subsequent_indent
            # Break the long word into pieces
            remaining = word
            iwidth = visible_width(indent)
            while remaining:
                room = max(width - iwidth, 1)
                lines.append(indent + remaining[:room])
                remaining = remaining[room:]
                indent = subsequent_indent
                iwidth = visible_width(indent)
            cur = []
            cur_width = iwidth
        else:
            if cur:
                lines.append(indent + " ".join(cur))
                indent = subsequent_indent
            cur = [word]
            cur_width = visible_width(indent) + wlen
    if cur:
        lines.append(indent + " ".join(cur))
    return lines


def fill(text: str, width: int, **kwargs) -> str:
    """Wrap text and join lines with newlines."""
    return "\n".join(wrap(text, width, **kwargs))


def shorten(text: str, width: int, *, placeholder: str = " [...]") -> str:
    """Collapse text to a single line, truncating with placeholder if needed."""
    if not isinstance(text, str):
        raise WrapError(f"text must be str, got {type(text).__name__}")
    width = _validate_width(width)
    if not isinstance(placeholder, str):
        raise WrapError("placeholder must be a string")
    one_line = " ".join(text.split())
    if visible_width(one_line) <= width:
        return one_line
    target = width - visible_width(placeholder)
    if target < 0:
        raise WrapError("width too small for placeholder")
    truncated = one_line
    while visible_width(truncated) > target:
        truncated = truncated.rsplit(" ", 1)[0] if " " in truncated else truncated[:-1]
    return truncated + placeholder
