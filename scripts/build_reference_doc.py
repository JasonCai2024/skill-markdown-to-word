#!/usr/bin/env python3

from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DOC = SCRIPT_DIR.parent / "assets" / "reference.docx"


def set_style_font(style, east_asia, ascii_font=None, size=None, bold=None, color=None):
    font = style.font
    ascii_font = ascii_font or east_asia
    font.name = ascii_font
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), east_asia)
    rfonts.set(qn("w:cs"), ascii_font)
    if size is not None:
        font.size = Pt(size)
    if bold is not None:
        font.bold = bold
    if color is not None:
        hex_value = str(color)
        font.color.rgb = color
        color_element = rpr.find(qn("w:color"))
        if color_element is None:
            color_element = OxmlElement("w:color")
            rpr.append(color_element)
        color_element.set(qn("w:val"), hex_value)
        for attr in ("w:themeColor", "w:themeTint", "w:themeShade"):
            qname = qn(attr)
            if color_element.get(qname) is not None:
                del color_element.attrib[qname]


def ensure_style(doc, name, style_type, base_style=None):
    try:
        style = doc.styles[name]
    except KeyError:
        style = doc.styles.add_style(name, style_type)
    if base_style is not None:
        style.base_style = base_style
    return style


def configure_document():
    doc = Document()

    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.48)
    section.right_margin = Cm(2.48)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)

    normal = doc.styles["Normal"]
    set_style_font(normal, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = normal.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Pt(24)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

    body_text = ensure_style(doc, "Body Text", WD_STYLE_TYPE.PARAGRAPH, normal)
    set_style_font(body_text, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = body_text.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Pt(24)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

    first_paragraph = ensure_style(doc, "First Paragraph", WD_STYLE_TYPE.PARAGRAPH, body_text)
    set_style_font(first_paragraph, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = first_paragraph.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Pt(24)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

    block_text = ensure_style(doc, "Block Text", WD_STYLE_TYPE.PARAGRAPH, body_text)
    set_style_font(block_text, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = block_text.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Pt(24)
    pf.left_indent = Pt(0)
    pf.right_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

    quote = ensure_style(doc, "Quote", WD_STYLE_TYPE.PARAGRAPH, body_text)
    set_style_font(quote, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = quote.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Pt(24)
    pf.left_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

    heading1 = doc.styles["Heading 1"]
    set_style_font(heading1, east_asia="SimHei", ascii_font="Times New Roman", size=15.5, bold=True, color=RGBColor(0, 0, 0))
    pf = heading1.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    heading2 = doc.styles["Heading 2"]
    set_style_font(heading2, east_asia="SimHei", ascii_font="Times New Roman", size=14, bold=True, color=RGBColor(0, 0, 0))
    pf = heading2.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    heading3 = doc.styles["Heading 3"]
    set_style_font(heading3, east_asia="SimHei", ascii_font="Times New Roman", size=12, bold=True, color=RGBColor(0, 0, 0))
    pf = heading3.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    table_style = doc.styles["Table Grid"]
    set_style_font(table_style, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))

    table_para = ensure_style(doc, "Table Paragraph", WD_STYLE_TYPE.PARAGRAPH, normal)
    set_style_font(table_para, east_asia="SimSun", ascii_font="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0))
    pf = table_para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    # Add a sample paragraph so Word keeps style definitions.
    p = doc.add_paragraph("样式模板初始化", style=body_text)
    p.runs[0].font.hidden = True

    OUTPUT_DOC.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_DOC))
    print(f"Generated reference doc: {OUTPUT_DOC}")


if __name__ == "__main__":
    configure_document()
