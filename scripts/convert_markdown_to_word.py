#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

from fix_md_for_word import process_markdown_file
from postprocess_docx import process_docx


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_REFERENCE_DOC = SKILL_DIR / "assets" / "reference.docx"


def run_pandoc(input_md: Path, output_docx: Path, reference_doc: Path) -> None:
    command = [
        "pandoc",
        str(input_md),
        "-o",
        str(output_docx),
        "--standalone",
        f"--resource-path={input_md.parent}",
        f"--reference-doc={reference_doc}",
    ]
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to Word using the skill workflow."
    )
    parser.add_argument("input_md", help="Path to the input Markdown file.")
    parser.add_argument(
        "output_docx",
        nargs="?",
        help="Optional output .docx path. Defaults to the input filename with a .docx extension.",
    )
    parser.add_argument(
        "--attachments-folder",
        help="Attachments folder path to inject into image references. Defaults to ./attachments relative to the input file.",
    )
    parser.add_argument(
        "--reference-doc",
        help="Optional reference .docx style template. Defaults to the bundled assets/reference.docx.",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep the generated .for_word.md temporary file.",
    )
    parser.add_argument(
        "--skip-postprocess",
        action="store_true",
        help="Skip the DOCX table post-processing step.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_md = Path(args.input_md).resolve()
    if not input_md.exists():
        print(f"Input Markdown file not found: {input_md}")
        return 1

    output_docx = (
        Path(args.output_docx).resolve()
        if args.output_docx
        else input_md.with_suffix(".docx")
    )
    output_docx.parent.mkdir(parents=True, exist_ok=True)

    attachments_folder = args.attachments_folder or "./attachments"
    temp_md = input_md.with_suffix(".for_word.md")
    reference_doc = (
        Path(args.reference_doc).resolve()
        if args.reference_doc
        else DEFAULT_REFERENCE_DOC.resolve()
    )

    if not reference_doc.exists():
        print(f"Reference DOCX not found: {reference_doc}")
        return 1

    generated = process_markdown_file(
        str(input_md),
        attachments_folder,
        str(temp_md),
    )
    if not generated:
        return 1

    try:
        run_pandoc(temp_md, output_docx, reference_doc)
        if not args.skip_postprocess:
            process_docx(str(output_docx))
    except subprocess.CalledProcessError as exc:
        print(f"Pandoc failed with exit code {exc.returncode}")
        return exc.returncode or 1
    finally:
        if not args.keep_temp and temp_md.exists():
            temp_md.unlink()

    print(f"Generated Word document: {output_docx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
