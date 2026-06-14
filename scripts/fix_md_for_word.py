#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from xml.etree import ElementTree as ET


IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.tif'}
TABLE_BLOCK_RE = re.compile(r'<table\b.*?</table>', re.IGNORECASE | re.DOTALL)


def process_markdown_file(input_file, attachments_folder, output_file=None):
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在: {input_file}")
        return None

    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = base + ".for_word" + ext

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = convert_wiki_links_to_images(content, attachments_folder)
    content = convert_html_tables(content)

    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print(f"已生成临时文件: {output_file}")
    return output_file


def convert_wiki_links_to_images(content, attachments_folder):
    wiki_image_pattern = r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'

    def replace_wiki_link(match):
        filename = match.group(1).strip()
        title = match.group(2).strip() if match.group(2) else ''

        _, ext = os.path.splitext(filename)
        ext_lower = ext.lower()

        if ext_lower in IMAGE_EXTENSIONS:
            relative_path = os.path.join(attachments_folder, filename).replace('\\', '/')
            return f'![{title}]({relative_path})' if title else f'![]({relative_path})'

        return f'[文件: {filename}]'

    content = re.sub(wiki_image_pattern, replace_wiki_link, content)
    content = convert_relative_image_paths(content, attachments_folder)
    return content


def convert_relative_image_paths(content, attachments_folder):
    pattern = r'!\[([^\]]*)\]\(([^/)]+\.[a-zA-Z]{3,4})\)'

    def replace_relative_path(match):
        alt_text = match.group(1).strip()
        filename = match.group(2).strip()

        ext = filename.lower().split('.')[-1]
        if f'.{ext}' in IMAGE_EXTENSIONS:
            attachments_prefix = attachments_folder.replace('\\', '/').lstrip('./')
            normalized = filename.replace('\\', '/')
            if not normalized.startswith(attachments_prefix):
                relative_path = os.path.join(attachments_folder, filename).replace('\\', '/')
                return f'![{alt_text}]({relative_path})' if alt_text else f'![]({relative_path})'

        return match.group(0)

    return re.sub(pattern, replace_relative_path, content)


def convert_html_tables(content):
    return TABLE_BLOCK_RE.sub(replace_table_block, content)


def replace_table_block(match):
    table_html = match.group(0)
    markdown_table = html_table_to_pipe_table(table_html)
    if markdown_table is None:
        return table_html
    return "\n" + markdown_table + "\n"


def html_table_to_pipe_table(table_html):
    try:
        root = ET.fromstring(f"<root>{table_html}</root>")
    except ET.ParseError:
        return None

    table = root.find('table')
    if table is None:
        return None

    rows = build_grid(table)
    if not rows:
        return None

    column_count = max(len(row) for row in rows)
    normalized_rows = [pad_row(row, column_count) for row in rows]

    # 第一行作为表头，和 Pandoc/Word 的兼容性最好
    header = normalized_rows[0]
    body = normalized_rows[1:] if len(normalized_rows) > 1 else [[""] * column_count]

    return render_pipe_table(header, body)


def build_grid(table):
    grid = []
    rowspan_state = {}

    tr_elements = table.findall('.//tr')
    for row_index, tr in enumerate(tr_elements):
        row = []
        col_index = 0

        while col_index in rowspan_state:
            cell_info = rowspan_state[col_index]
            row.append(cell_info['text'])
            cell_info['remaining'] -= 1
            if cell_info['remaining'] <= 0:
                del rowspan_state[col_index]
            col_index += 1

        for cell in list(tr):
            tag = strip_ns(cell.tag).lower()
            if tag not in ('td', 'th'):
                continue

            while col_index in rowspan_state:
                cell_info = rowspan_state[col_index]
                row.append(cell_info['text'])
                cell_info['remaining'] -= 1
                if cell_info['remaining'] <= 0:
                    del rowspan_state[col_index]
                col_index += 1

            cell_text = normalize_cell_text(extract_inline_text(cell)).strip()
            colspan = parse_span(cell.attrib.get('colspan'))
            rowspan = parse_span(cell.attrib.get('rowspan'))

            for offset in range(colspan):
                row.append(cell_text)
                if rowspan > 1:
                    rowspan_state[col_index + offset] = {
                        'text': cell_text,
                        'remaining': rowspan - 1,
                    }
            col_index += colspan

        while col_index in rowspan_state:
            cell_info = rowspan_state[col_index]
            row.append(cell_info['text'])
            cell_info['remaining'] -= 1
            if cell_info['remaining'] <= 0:
                del rowspan_state[col_index]
            col_index += 1

        grid.append(row)

    while rowspan_state:
        row = []
        col_index = 0
        max_col = max(rowspan_state)
        while col_index <= max_col:
            if col_index in rowspan_state:
                cell_info = rowspan_state[col_index]
                row.append(cell_info['text'])
                cell_info['remaining'] -= 1
                if cell_info['remaining'] <= 0:
                    del rowspan_state[col_index]
            else:
                row.append("")
            col_index += 1
        grid.append(row)

    return grid


def parse_span(value):
    try:
        span = int(value)
        return span if span > 0 else 1
    except (TypeError, ValueError):
        return 1


def pad_row(row, width):
    padded = list(row)
    while len(padded) < width:
        padded.append("")
    return padded


def render_pipe_table(header, body):
    header_line = "| " + " | ".join(escape_pipe(cell) for cell in header) + " |"
    separator_line = "| " + " | ".join("---" for _ in header) + " |"
    body_lines = [
        "| " + " | ".join(escape_pipe(cell) for cell in row) + " |"
        for row in body
    ]
    return "\n".join([header_line, separator_line] + body_lines)


def escape_pipe(text):
    return text.replace("|", r"\|")


def normalize_cell_text(text):
    text = re.sub(r'\s*\n\s*', '<br />', text.strip())
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def extract_inline_text(element):
    parts = []

    if element.text:
        parts.append(element.text)

    for child in list(element):
        tag = strip_ns(child.tag).lower()

        if tag == 'strong':
            inner = extract_inline_text(child).strip()
            parts.append(f"**{inner}**" if inner else "")
        elif tag in ('b',):
            inner = extract_inline_text(child).strip()
            parts.append(f"**{inner}**" if inner else "")
        elif tag in ('em', 'i'):
            inner = extract_inline_text(child).strip()
            parts.append(f"*{inner}*" if inner else "")
        elif tag == 'br':
            parts.append('\n')
        elif tag in ('p', 'blockquote', 'div'):
            inner = extract_inline_text(child).strip()
            if inner:
                if parts and not parts[-1].endswith('\n'):
                    parts.append('\n')
                parts.append(inner)
                parts.append('\n')
        else:
            inner = extract_inline_text(child)
            if inner:
                parts.append(inner)

        if child.tail:
            parts.append(child.tail)

    return ''.join(parts)


def strip_ns(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag


def main():
    if len(sys.argv) < 2:
        print("用法: python fix_md_for_word.py <input.md> [attachments_folder] [output.md]")
        print("  input.md: 要处理的Markdown文件路径")
        print("  attachments_folder: 图片文件夹路径 (默认: ./attachments)")
        print("  output.md: 预处理后的临时Markdown文件路径 (默认: input.for_word.md)")
        sys.exit(1)

    input_file = sys.argv[1]
    attachments_folder = sys.argv[2] if len(sys.argv) > 2 else "./attachments"
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    generated = process_markdown_file(input_file, attachments_folder, output_file)
    sys.exit(0 if generated else 1)


if __name__ == "__main__":
    main()
