#!/usr/bin/env python3
"""Check that unattended mode is declared in both of its places, or in neither.

A skill that supports unattended mode (run by the paad-delegate agent, with no
person present) carries a short paragraph near the top, opening with
UNATTENDED_MARKER, and a section, headed UNATTENDED_SECTION, that holds the
defaults and stops. One without the other is a skill that half-supports the
mode, so it fails.

The paragraph also carries UNATTENDED_OVERRIDE verbatim. The shared
configuration and security paragraphs stay unchanged, because the shipped tree
must keep passing check-config and check_security.py; this sentence is what
overrides them under the delegate. A skill without the paragraph is not
checked, so the shipped tree passes.
"""

import pathlib
import sys
import tempfile

UNATTENDED_MARKER = "**Unattended mode:**"
UNATTENDED_SECTION = "## Unattended mode"
UNATTENDED_OVERRIDE = (
    "When this skill runs under the delegate, the Configuration paragraph above applies only to a "
    "config file the dispatch prompt names, each other config file found is listed as not followed, "
    "any Security findings paragraph above writes no security file and asks nothing, the result "
    "format's line order governs, and the \"Unattended mode\" section below governs the run."
)


def check(skills_dir):
    """Return a list of problem strings; empty means the tree passes."""
    problems = []
    for d in sorted(pathlib.Path(skills_dir).iterdir()):
        if not d.is_dir():
            continue
        try:
            text = (d / "SKILL.md").read_text(encoding="utf-8")
        except OSError as e:
            problems.append(f"{d.name}: cannot read SKILL.md ({e.strerror or e})")
            continue
        has_marker = UNATTENDED_MARKER in text
        has_section = any(line.rstrip() == UNATTENDED_SECTION for line in text.splitlines())
        if has_marker and not has_section:
            problems.append(f'{d.name} carries the unattended paragraph but has no "{UNATTENDED_SECTION}" section')
        elif has_section and not has_marker:
            problems.append(f'{d.name} has a "{UNATTENDED_SECTION}" section but does not carry the unattended paragraph')
        if has_marker and _normalize(UNATTENDED_OVERRIDE) not in _normalize(_paragraph(text)):
            problems.append(f"{d.name}'s unattended paragraph lacks the override sentence")
    return problems


def _paragraph(text):
    """The unattended paragraph: from the marker to the next blank line."""
    start = text.index(UNATTENDED_MARKER)
    end = text.find("\n\n", start)
    return text[start:] if end == -1 else text[start:end]


def _normalize(text):
    return " ".join(text.split())


def _write_skill(root, name, body):
    (root / name).mkdir()
    (root / name / "SKILL.md").write_text(body, encoding="utf-8")


def self_test():
    head = "---\nname: {0}\n---\n\n"
    paragraph = f"{UNATTENDED_MARKER} this skill runs under the delegate. {UNATTENDED_OVERRIDE}\n\n"
    section = f"{UNATTENDED_SECTION}\n\nDefaults and stops.\n"
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        _write_skill(root, "vibe", head.format("vibe") + "nothing here\n")
        assert check(root) == [], check(root)

        _write_skill(root, "pushback", head.format("pushback") + paragraph + section)
        assert check(root) == [], check(root)

        _write_skill(root, "alignment", head.format("alignment") + paragraph)
        assert check(root) == [
            'alignment carries the unattended paragraph but has no "## Unattended mode" section'
        ], check(root)
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + section, encoding="utf-8")
        assert check(root) == [
            "alignment has a \"## Unattended mode\" section but does not carry the unattended paragraph"
        ], check(root)
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + paragraph + section, encoding="utf-8")
        assert check(root) == [], check(root)

        # The override sentence must sit in the unattended paragraph itself, verbatim.
        no_override = f"{UNATTENDED_MARKER} this skill runs under the delegate.\n\n"
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + no_override + section, encoding="utf-8")
        assert check(root) == ["alignment's unattended paragraph lacks the override sentence"], check(root)
        elsewhere = no_override + UNATTENDED_OVERRIDE + "\n\n"
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + elsewhere + section, encoding="utf-8")
        assert check(root) == ["alignment's unattended paragraph lacks the override sentence"], check(root)
        reworded = paragraph.replace("asks nothing", "never asks")
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + reworded + section, encoding="utf-8")
        assert check(root) == ["alignment's unattended paragraph lacks the override sentence"], check(root)
        (root / "alignment" / "SKILL.md").write_text(head.format("alignment") + paragraph + section, encoding="utf-8")
        assert check(root) == [], check(root)
        # vibe, with no unattended paragraph, was never checked for the sentence above.

        # A skill folder whose SKILL.md cannot be read is a failure, never a pass.
        (root / "broken").mkdir()
        (root / "broken" / "SKILL.md").mkdir()
        assert any(p.startswith("broken: cannot read SKILL.md") for p in check(root)), check(root)
    print("check_unattended.py: self-tests passed")


def main(argv):
    if argv[1:] == ["--self-test"]:
        self_test()
        return 0
    if len(argv) != 2:
        print("usage: check_unattended.py <skills-dir> | --self-test", file=sys.stderr)
        return 2
    tree = pathlib.Path(argv[1]).parent
    problems = check(argv[1])
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        return 1
    print(f"{tree}: unattended mode is declared in both places or neither, in every skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
