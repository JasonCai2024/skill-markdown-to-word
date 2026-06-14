---
name: skill-markdown-to-word
description: Converts Markdown files to Word .docx files with Pandoc, attachment path fixes, reference styles, and optional table post-processing. Use when turning .md documents into Word files while preserving images, tables, and editable document structure.
disable-model-invocation: true
user-invocable: true
argument-hint: [markdown-file]
---

# Markdown To Word

## Goal

Convert a Markdown document into a Word `.docx` file while preserving text, images, and tables as reliably as possible.

## Scope

Use this skill for Markdown-to-Word conversion workflows that rely on:

- `pandoc`
- image assets stored in an `attachments/` folder
- a reference Word style document
- optional DOCX table post-processing

Do not use this skill for:

- PDFs or non-Markdown inputs
- direct HTML-to-Word conversion
- cases where `pandoc` is unavailable and no alternative tool is approved

## Required Inputs

Provide:

1. The source Markdown file path.
2. The target `.docx` output path if it should not use the source filename.
3. Whether the Markdown uses an `attachments/` folder for images.
4. Whether the output should use the bundled `reference.docx`.

## Workflow

1. Read the source Markdown file and identify the working directory.
2. Preprocess the Markdown with `scripts/fix_md_for_word.py` to normalize image paths and convert supported HTML tables into pipe tables.
3. Run `pandoc` against the preprocessed Markdown and output a `.docx` file.
4. Use `assets/reference.docx` as the reference document unless the user provides another style document.
5. Run `scripts/postprocess_docx.py` after conversion so Word tables receive stable borders and baseline formatting.
6. Remove the temporary `.for_word.md` file unless the user asks to keep it.

## Decision Rules

1. If the Markdown contains Obsidian wiki image links, convert them before calling `pandoc`.
2. If the document contains HTML tables, attempt conversion during preprocessing instead of feeding raw HTML to Word directly.
3. If `pandoc` is missing, stop and report the missing dependency instead of improvising a weaker conversion path.
4. If the user does not provide an output path, write the `.docx` next to the source Markdown.
5. If the document has no tables, `postprocess_docx.py` may still be called because it safely no-ops when no tables exist.

## Output Requirements

Return:

1. The input Markdown file path.
2. The output Word file path.
3. Whether preprocessing, Pandoc conversion, and DOCX post-processing succeeded.
4. Any skipped steps or dependency issues.

## Validation

Check:

1. The output `.docx` file exists.
2. The temporary preprocessed Markdown was handled as requested.
3. Images resolve through the expected attachments path.
4. The conversion command used the intended reference style document.

## Fallback

If deterministic execution is needed, run:

`scripts/convert_markdown_to_word.py <input.md> [output.docx]`

If the result has table rendering issues, inspect:

`references/workflow.md`

If the style template needs regeneration, use:

`scripts/build_reference_doc.py`

## Examples

- Convert `report.md` into `report.docx` and keep the attachments working.
- Turn this Obsidian Markdown note into a styled Word file.
- Export this Markdown proposal to Word and preserve editable tables.
