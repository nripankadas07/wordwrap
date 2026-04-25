"""wordwrap — ANSI-aware paragraph wrap, fill, and shorten with hanging indents and wide-character support.

Public API:

* :func:`wrap`           — wrap text to a width returning a list of lines.
* :func:`fill`           — wrap then join with newlines.
* :func:`shorten`        — collapse to a single line, truncate with placeholder.
* :func:`visible_width`  — measure printed width (ANSI-aware, CJK-aware).
* :func:`strip_ansi`     — remove CSI/OSC escape sequences.
* :class:`WrapError`     — raised on invalid input (ValueError subclass).
"""

from __future__ import annotations

from ._core import (
    WrapError,
    fill,
    shorten,
    strip_ansi,
    visible_width,
    wrap,
)

__all__ = [
    "WrapError",
    "fill",
    "shorten",
    "strip_ansi",
    "visible_width",
    "wrap",
]

__version__ = "0.1.0"
