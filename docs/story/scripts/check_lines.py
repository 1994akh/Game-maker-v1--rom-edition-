"""Check the story scripts against the message box's line budget (docs/story/scripts/README.md).

Usage:  python -X utf8 docs/story/scripts/check_lines.py [FILE.md ...]
        (no files: every script page in this folder except README.md)

What it reads, the way README.md writes it:
- A page of game text starts with **Speaker:** at the start of a line (optionally indented under a list item).
  The lines below it, up to the next blank line, are the box's lines.
- A plain paragraph straight after a page (one blank line between) is the next page of the same speaker.
- Italic paragraphs (*...*) are stage directions; headings, tables and list items are not game text.
- A reply option is a numbered list item whose first quoted string is its label.

What it checks:
- every line fits LINE_MAX characters with the tokens at their longest ({HERO} as a 10-letter name);
- every page has at most PAGE_LINES lines;
- every reply label fits LABEL_MAX;
- only plain ASCII and é (the font's safe set), so no curly quotes, ellipsis characters or dashes;
- {HERO_SUBJ} is never at the start of a sentence (tokens are lower case) and never before is/was/has/does,
  which don't agree with "they".

Exit code 1 if anything fails, so a hook or a builder can run it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINE_MAX = 36
PAGE_LINES = 3
LABEL_MAX = 24
TOKEN_WIDTH = {
    "{HERO}": 10,
    "{HERO_SUBJ}": 4,
    "{HERO_OBJ}": 4,
    "{HERO_POSS}": 5,
    "{LEADER}": 10,
}
SPEAKER = re.compile(r"^(\s*)\*\*([^*]+?):\*\*\s?(.*)$")
LIST_ITEM = re.compile(r"^\s*(\d+\.|[-+])\s")
LABEL = re.compile(r'^\s*\d+\.\s+"([^"]+)"')
SAFE = re.compile(r"^[\x20-\x7eé]*$")
SUBJ_VERB = re.compile(r"\{HERO_SUBJ\}\s+(is|was|has|does|isn't|wasn't|hasn't|doesn't)\b")
SUBJ_START = re.compile(r"(^|[.!?]\s+)\{HERO_SUBJ\}")


def width(line: str) -> int:
    n = len(line)
    for tok, w in TOKEN_WIDTH.items():
        n += line.count(tok) * (w - len(tok))
    return n


def is_prose_start(text: str) -> bool:
    """A paragraph that can't be a continuation page: markup of any kind."""
    s = text.lstrip()
    return (s == "" or s.startswith(("*", "#", "|", ">", "```", "<!--", "_"))
            or bool(LIST_ITEM.match(s)) or bool(SPEAKER.match(text)))


def check_page(path: Path, start: int, speaker: str, lines: list[str], problems: list[str]) -> None:
    if speaker.endswith(" replies"):
        return
    if len(lines) > PAGE_LINES:
        problems.append(f"{path.name}:{start}: {speaker}: {len(lines)} lines on one page (max {PAGE_LINES})")
    for i, line in enumerate(lines):
        w = width(line)
        if w > LINE_MAX:
            problems.append(f"{path.name}:{start + i}: {speaker}: {w} chars (max {LINE_MAX}): {line}")
        if not SAFE.match(line):
            bad = "".join(sorted({c for c in line if not SAFE.match(c)}))
            problems.append(f"{path.name}:{start + i}: {speaker}: characters outside the font's safe set: {bad!r}")
    text = " ".join(lines)
    if SUBJ_VERB.search(text):
        problems.append(f"{path.name}:{start}: {speaker}: {{HERO_SUBJ}} before a verb that breaks with 'they'")
    if SUBJ_START.search(text):
        problems.append(f"{path.name}:{start}: {speaker}: {{HERO_SUBJ}} starts a sentence (tokens are lower case)")


def check_file(path: Path) -> tuple[int, list[str]]:
    problems: list[str] = []
    raw = path.read_text(encoding="utf-8").splitlines()
    pages = 0
    in_code = False
    i = 0
    last_speaker = ""   # the speaker whose page ended at the last blank line, for continuation pages
    last_indent = -1
    while i < len(raw):
        line = raw[i]
        if line.lstrip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue
        m_label = LABEL.match(line)
        if m_label:
            label = m_label.group(1)
            if width(label) > LABEL_MAX:
                problems.append(f"{path.name}:{i + 1}: reply label {width(label)} chars (max {LABEL_MAX}): {label}")
            if not SAFE.match(label):
                problems.append(f"{path.name}:{i + 1}: reply label has characters outside the safe set: {label}")
        m = SPEAKER.match(line)
        cont = (m is None and last_speaker != "" and not is_prose_start(line)
                and len(line) - len(line.lstrip()) == last_indent)
        if m or cont:
            if m:
                indent, speaker, first = len(m.group(1)), m.group(2).strip(), m.group(3)
                body = [first] if first.strip() else []
            else:
                indent, speaker, body = last_indent, last_speaker, [line.strip()]
            start = i + 1
            i += 1
            while i < len(raw) and raw[i].strip() != "":
                nxt = raw[i]
                if SPEAKER.match(nxt) or LIST_ITEM.match(nxt):
                    break
                body.append(nxt.strip())
                i += 1
            if speaker.endswith(" replies"):
                last_speaker, last_indent = "", -1
                continue
            check_page(path, start, speaker, body, problems)
            pages += 1
            last_speaker, last_indent = speaker, indent
            # a continuation page must follow after exactly one blank line
            if i < len(raw) and raw[i].strip() == "":
                i += 1
                continue
            last_speaker, last_indent = "", -1
            continue
        if line.strip() != "":
            last_speaker, last_indent = "", -1
        i += 1
    return pages, problems


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent
    files = [Path(a) for a in argv] or sorted(p for p in here.glob("*.md") if p.name != "README.md")
    total, all_problems = 0, []
    for f in files:
        n, probs = check_file(f)
        total += n
        all_problems += probs
        print(f"{f.name}: {n} pages, {len(probs)} problems")
    for p in all_problems:
        print("  " + p)
    print(f"{total} pages checked, {len(all_problems)} problems")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
