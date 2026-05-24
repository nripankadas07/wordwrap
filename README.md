# wordwrap

Zero-dependency, ANSI-aware paragraph wrap, fill, and shorten with hanging indents, wide-character (CJK) support, and graceful handling of zero-width / combining marks.

## Install

```bash
python -m pip install -e .
```

Requires Python 3.10+. No runtime dependencies.

## Quick example

```python
from wordwrap import wrap, fill, shorten, visible_width, strip_ansi

wrap("The quick brown fox jumps over the lazy dog", width=20)
# ["The quick brown fox", "jumps over the lazy", "dog"]

fill("hello world " * 5, width=24, initial_indent="   * ", subsequent_indent="     ")
# "   * hello world hello\n     world hello world\n     hello world"

shorten("a long sentence", width=10, placeholder="...")
# "a long..."

visible_width("\x1b[31mred\x1b[0m text")     # 8 (ANSI escapes ignored)
visible_width("こんにちは")                     # 10 (each CJK char counts 2)
strip_ansi("\x1b[1;33mbold yellow\x1b[0m")    # "bold yellow"
```

## Quality

- **71 tests, 100% line coverage**
- Zero runtime dependencies
- ANSI-aware: visible width measured ignoring CSI/OSC escapes
- CJK-aware: wide East-Asian characters count 2 cells; combining marks count 0
- Active SGR state preserved across line breaks

## API

### `wrap(text, width, *, initial_indent="", subsequent_indent="", break_long_words=True, tabsize=8, drop_whitespace=True) -> list[str]`
Wrap *text* to *width* columns. Returns a list of output lines.

### `fill(text, width, **kwargs) -> str`
Wrap, then join lines with newlines.

### `shorten(text, width, *, placeholder=" [...]") -> str`
Collapse to a single line and truncate with *placeholder* if needed.

### `visible_width(text) -> int`
Measure the printed width of *text* (ANSI escapes ignored, CJK as 2, combining as 0).

### `strip_ansi(text) -> str`
Remove CSI / OSC / SGR escape sequences from *text*.

### `WrapError`
Subclass of `ValueError`.

## Running tests

```bash
pip install -e ".[dev]"
pytest                           # 71 tests
pytest --cov=wordwrap            # 100% line coverage
```

## License

MIT
