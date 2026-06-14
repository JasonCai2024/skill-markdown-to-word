# Markdown To Word — Install & Setup

This skill is intentionally minimal: no remote API, no credential, no Python package install step beyond a system Python 3 and Pandoc.

## 1. Prerequisites

| Tool   | Version | Why                                          |
| ------ | ------- | -------------------------------------------- |
| Python | 3.8+    | runs `scripts/*.py`                          |
| Pandoc | 2.19+   | does the actual Markdown → DOCX conversion   |

Verify locally:

```bash
python --version
pandoc --version
```

## 2. Install the skill

### Option A — Claude Code & OpenCode (recommended)

Copy the entire `skill-markdown-to-word/` folder (not just `SKILL.md`) into one of these:

- Project-level: `<your-project>/.claude/skills/skill-markdown-to-word/`
- Global:        `~/.claude/skills/skill-markdown-to-word/`

### Option B — OpenCode only

You may also use:

- `<your-project>/.opencode/skills/skill-markdown-to-word/`
- `~/.config/opencode/skills/skill-markdown-to-word/`

But Option A is recommended because OpenCode also reads `.claude/skills/`, so one copy serves both tools.

### Option C — Optional Claude Code legacy command

To maximise the chance of `skill-markdown-to-word` showing up in Claude Code's `/` completion list, you can additionally drop this minimal file at:

`~/.claude/commands/skill-markdown-to-word.md`

```markdown
---
description: Converts Markdown files to Word .docx via Pandoc, with image path fixes and DOCX table post-processing.
argument-hint: [markdown-file]
---

Convert the given Markdown file to Word using the bundled skill.

If no input path is provided in `$ARGUMENTS`, ask for it and stop.

Prefer using:

`~/.claude/skills/skill-markdown-to-word/scripts/convert_markdown_to_word.py <input.md> [output.docx]`
```

## 3. Reload & verify

- **Claude Code**: restart the CLI or start a new session, then type `/` and look for `skill-markdown-to-word`.
- **OpenCode**: restart or open a new session; the skill should appear in the skill list.

## 4. Uninstall

Delete the folder you copied in step 2 (and the optional command file from step 2C if you created it). No system-level artefacts are left behind.
