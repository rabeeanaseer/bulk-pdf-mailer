"""
pdf_generator.py
----------------
Builds a single PDF report from one row of data using ReportLab.

Each row (a dict of column_name -> value) becomes one PDF file.
Customize `build_pdf()` below to change the look of the report.
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TitleStyle",
    parent=styles["Heading1"],
    fontSize=20,
    textColor=colors.HexColor("#1F2A44"),
    spaceAfter=6,
)

SUBTITLE_STYLE = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Normal"],
    fontSize=10,
    textColor=colors.HexColor("#6B7280"),
    spaceAfter=16,
)

BODY_STYLE = styles["Normal"]


def build_pdf(row: dict, output_path: str, name_field: str = "Name",
              report_heading: str = "Report") -> str:
    """
    Build a single PDF for one data row.

    Args:
        row: dict mapping column name -> value for this row (e.g. from a
             pandas Series via .to_dict()).
        output_path: full path (including filename) to write the PDF to.
        name_field: which column to use as the "recipient name" in the title.
        report_heading: heading text shown at the top of the report.

    Returns:
        The output_path, for convenience/chaining.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title=report_heading,
    )

    elements = []

    recipient_name = str(row.get(name_field, "")).strip() or "Unknown"

    # --- Header ---
    elements.append(Paragraph(report_heading, TITLE_STYLE))
    elements.append(
        Paragraph(
            f"Prepared for <b>{recipient_name}</b> &nbsp;|&nbsp; "
            f"Generated on {datetime.now().strftime('%d %B %Y')}",
            SUBTITLE_STYLE,
        )
    )
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#E5E7EB")))
    elements.append(Spacer(1, 16))

    # --- Data table: every column in the row becomes a line item ---
    table_data = [["Field", "Value"]]
    for key, value in row.items():
        if value is None or (isinstance(value, float) and str(value) == "nan"):
            value = ""
        table_data.append([str(key), str(value)])

    table = Table(table_data, colWidths=[5 * cm, 10.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F2A44")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(table)

    elements.append(Spacer(1, 24))
    elements.append(
        Paragraph(
            "This report was generated automatically. "
            "Please contact us if you notice any discrepancies.",
            ParagraphStyle("Footer", parent=BODY_STYLE, fontSize=8, textColor=colors.grey),
        )
    )

    doc.build(elements)
    return output_path
